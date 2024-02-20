import logging
import sys
import asyncio
from appconfig import Config

from newssite import SiteSpiegel, SiteZeit
from storage import MongoStorage

sites = [SiteSpiegel(), SiteZeit()]


async def crawl_and_store(storage, site, loop_delay_minutes=10):
    while True:
        async for x in site.linked_articles(storage):
            if x.headline:
                logging.debug(f"Storing article {x.headline} @ {x.url}")
                storage.store_article(x)

        logging.debug(f"Sleeping {loop_delay_minutes} minutes before looping")
        asyncio.sleep(60*loop_delay_minutes)


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] %(asctime)s -- %(message)s -- %(module)s:%(lineno)s",
        stream=sys.stdout,
        force=True,
    )
    logging.info("Starting crawler...")
    config = Config()
    storage = MongoStorage(config.mongo_host, 27017,
                           config.mongo_user, config.mongo_password)
    await asyncio.gather(
        *map(lambda site: crawl_and_store(storage, site), sites)
    )


asyncio.run(main())
