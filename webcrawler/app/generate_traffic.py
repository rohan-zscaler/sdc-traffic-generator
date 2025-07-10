import asyncio
import logging
import os
import random
import threading
from urllib.parse import urlparse

import playwright.async_api
import settings
from playwright.async_api import Page, async_playwright
from utilities import (browser_launch_options, filter_urls,
                       page_launch_options, setup_logger)
import time

if settings.DEBUG:
    logger = setup_logger(name=__name__, level=logging.DEBUG)
else:
    logger = setup_logger(name=__name__, level=logging.INFO)


lastUpdate = time.time()

def didSomething():
    global lastUpdate
    seconds_since_last_call = time.time() - lastUpdate
    logger.info(f"seconds_since_last_call: {seconds_since_last_call}")
    lastUpdate = time.time()

def my_method():
    global lastUpdate
    seconds_since_last_call = time.time() - lastUpdate
    logger.info(f"seconds_since_last_call2: {seconds_since_last_call}")
    if seconds_since_last_call > 70:
        logger.info(f"Time to go!!")
        os._exit(1)

    threading.Timer(10.0, my_method).start()

# Call the method for the first time
my_method()

async def generate_traffic(url: str, surf_depth: int = 1):
    """
    Call URL to surf_depth and only further browse based on href_filter constraints.

    Args:
        url: (str) URL to call.
        surf_depth: (int) How deep to recurse (aka surf further links).

    """
    # Pause browsing to simulate a user.
    didSomething()
    sleep_seconds = round(random.uniform(settings.SLEEP_MIN, settings.SLEEP_MAX), 2)
    logger.info(f"Sleeping {sleep_seconds}s before rendering {url}. {surf_depth=}")
    await asyncio.sleep(sleep_seconds)

    surf_depth = surf_depth - 1
    async with async_playwright() as p:
        browser = await p.chromium.launch(**browser_launch_options())
        page = await browser.new_page(**page_launch_options())

        try:
            await page.goto(url)
            await page.wait_for_load_state("networkidle")

            page = await zia_login(page=page)
            await page.wait_for_load_state("load")

            logger.debug(f"Title of Page: {await page.title()}")
            await page.wait_for_load_state("networkidle")

            parsed_url = urlparse(page.url)
            if "duckduckgo.com" in parsed_url.hostname:
                results_links = await page.eval_on_selector_all(
                    settings.DDG_SEARCH_URL_LINKS,
                    "elements => elements.map(element => element.href)",
                )
            else:
                results_links = await page.eval_on_selector_all(
                    settings.HREF_QUERY_STRING,
                    "elements => elements.map(element => element.href)",
                )
        except (
            playwright.async_api.TimeoutError,
            playwright.async_api.Error,
        ) as e:
            results_links = []
            logger.debug(f"Rendering {url} failed: {e}")

    if surf_depth > 0:
        for link in filter_urls(urls=results_links):
            await generate_traffic(
                url=link,
                surf_depth=surf_depth,
            )
    else:
        logger.debug(f"\t##### Surfing limit reached. Ending this crawl path. #####")

async def aup(page: Page):
    """
    Test for Acceptable Usage Policy page, click "I Agree", and return.
    """
    await page.wait_for_load_state("load")
    if "Acceptable Usage Policy" == await page.title():
        logger.debug(f"AUP page detected. Agreeing to whatever is says.")
        await page.locator(f"input[name={settings.AUP_BUTTON}]").click()
    else:
        logger.debug(f"AUP page not detected or already accepted. Continuing on.")
    return page


async def zia_login(page: Page):
    """
    Log into ZIA Authentication.

    :param page: Playwright Page Object.
    :return: Page object.
    """

    selected_user = random.choice(settings.USERS)
    username = selected_user.get("username")
    password = selected_user.get("password", settings.DEFAULT_PASSWORD)
    logger.debug(f"Using user {username} for this browser session.")
    await page.wait_for_load_state("load")
    parsed_url = urlparse(page.url)
    # Detect which idp is being used:

    if settings.OKTA_LOGIN_URL in page.url:
        didSomething()
        logger.debug("Authenticating using Okta as IDP.")
        try:
            # Needs validated/checked as I don't have OKTA to test against atm.
            await page.locator(settings.OKTA_USERNAME).fill(username)
            await page.locator(settings.OKTA_SIGNIN_SUBMIT).click()

            await page.locator(settings.OKTA_PASSWORD).fill(password)
            await page.locator(settings.OKTA_SIGNIN_SUBMIT).click()
        except playwright.async_api.TimeoutError as e:
            logger.info(f"Okta IDP selected but the authentication workflow failed: {e}")
    elif settings.MICROSOFT_LOGIN_URL in page.url:
        logger.debug("Authenticating using Microsoft as IDP.")
        didSomething()
        try:
            await page.locator(settings.MICROSOFT_USERNAME).fill(username)
            await page.locator(settings.MICROSOFT_SIGNIN_SUBMIT).click()

            await asyncio.sleep(1)
            await page.locator(settings.MICROSOFT_PASSWORD).fill(password)
            await page.locator(settings.MICROSOFT_SIGNIN_SUBMIT).click()

            await page.locator(settings.MICROSOFT_STAY_SIGNED_IN).click()
        except playwright.async_api.TimeoutError as e:
            logger.warning(f"MS IDP selected but the authentication workflow failed: {e}")
    elif any(
        substring in settings.ZIA_LOCAL_URLS
        for substring in parsed_url.hostname.split(".")
    ):  # See if URL contains one of the zscaler domains.
        logger.info("Authenticating using ZIA Local as IDP.")
        didSomething()
        try:
            await page.locator(settings.ZIA_LOCAL_USERNAME).fill(username)
            await page.locator(settings.ZIA_LOCAL_USERNAME).press("Enter")
            await page.locator(settings.ZIA_LOCAL_PASSWORD).click()

            await page.locator(settings.ZIA_LOCAL_PASSWORD).fill(password)
            await page.locator(settings.ZIA_LOCAL_SIGNIN_SUBMIT).click()

            await page.locator("text=Please wait a moment...").wait_for(state="hidden")
        except playwright.async_api.TimeoutError as e:
            logger.info(f"ZIA Local IDP selected but the authentication workflow failed: {e}")
    else:
        logger.warning("ZIA sign-in page not detected. Moving on.")

    # Check for Acceptable Usage Policy Page.
    page = await aup(page=page)
    await page.wait_for_load_state("load")

    return page
