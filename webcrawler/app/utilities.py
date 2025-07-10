import logging
import random
from urllib.parse import urlparse

import settings


def setup_logger(name, level=logging.INFO):
    """To set up as many loggers as you want"""

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="{asctime} {name} {levelname} {message}",
        datefmt="%Y%m%d %H:%M:%S",
        style="{",
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)

    logger.setLevel(level)

    return logger


def filter_urls(urls: list) -> list:
    """
    Take a list of URLs and cleanse them of domains we know we have issues web scraping.
    :param urls: list of urls
    :return: list of filtered urls
    """
    links = []
    for link in urls:
        link = link.lower()
        temp = urlparse(link)
        if (
            temp.scheme in ["http", "https"]
            and link != "javascript:;"
            and temp.hostname not in settings.EXCLUDED_DOMAINS
        ):
            logger.debug(f"{link} is permitted to be crawled.")
            links.append(link)
        else:
            logger.debug(f"{link} is EXCLUDED.")
    if len(links) > settings.LINKS_MAX_PER_PAGE:
        logger.debug(
            f"Links gathered exceeds MAX setting. Reducing to MAX link count."
        )

        # Instead of just truncating the list let's grab the "middle" of the list. This way we can hopefully miss some
        # header/footer links.
        delta = len(links) - settings.LINKS_MAX_PER_PAGE
        front = int(delta / 2)
        back = delta - front
        links = links[front:-back]
    return links


def browser_launch_options():
    # Setting the options we want all new browser objects to use.
    return {
        "headless": settings.HEADLESS,
        "slow_mo": settings.SLO_MO,
    }


def page_launch_options():
    # Setting the options we want all new page objects to use.
    return {
        "ignore_https_errors": settings.IGNORE_HTTPS_ERRORS,
        "user_agent": random.choice(settings.USER_AGENTS),
    }


if settings.DEBUG:
    logger = setup_logger(name=__name__, level=logging.DEBUG)
else:
    logger = setup_logger(name=__name__, level=logging.INFO)
