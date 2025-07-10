import asyncio
import logging
import random

import settings
from generate_traffic import generate_traffic
from utilities import setup_logger

if settings.DEBUG:
    logger = setup_logger(name=__name__, level=logging.DEBUG)
else:
    logger = setup_logger(name=__name__, level=logging.INFO)


async def main():
    total_renders = (
        len(settings.SEARCH_TERMS) + len(settings.CRAWL_URLS)
    ) * settings.LINKS_MAX_PER_PAGE**settings.SEARCH_DEPTH

    logger.info("##### Starting script #####")
    logger.info(
        f"Based on settings we will call up to {total_renders} webpages with a wait between each page."
    )
    logger.info(
        f"Estimated runtime will be between {total_renders * settings.SLEEP_MIN} and"
        f" {total_renders * settings.SLEEP_MAX} seconds."
    )

    # Load CRAWL_URLs list.
    all_urls = settings.CRAWL_URLS

    # Add search results URLs to list.
    random.shuffle(settings.SEARCH_TERMS)
    for search_term in settings.SEARCH_TERMS:
        # Search for search term to get URLs then render each of those URLs.
        all_urls.append(f"https://duckduckgo.com?q={search_term.replace(' ', '+')}")

    # Shuffle URLs to add "randomness" to page calls.
    random.shuffle(all_urls)
    logger.debug(f"{all_urls=}")

    # Time to render the URLs and get moar URLs (based on settings.SEARCH_DEPTH).
    tasks = [asyncio.create_task(generate_traffic(url=url, surf_depth=settings.SEARCH_DEPTH), name=url) for url in all_urls]
    for task in tasks:
        await task

    # Use the following if you want to run the searches in serial (instead of the tasks loop above).
    # for url in all_urls:
    #     await generate_traffic(url=url, surf_depth=settings.SEARCH_DEPTH)


if __name__ == "__main__":
    asyncio.run(main())
