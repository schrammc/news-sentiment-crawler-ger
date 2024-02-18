import logging
import sys
import asyncio
from appconfig import Config

from newssite import SiteSpiegel, SiteZeit
from storage import MongoStorage

sites = [SiteSpiegel(), SiteZeit()]


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] %(asctime)s -- %(message)s -- %(module)s:%(lineno)s",
        stream=sys.stdout,
        force=True,
    )
    logging.info("Starting crawler...")
    storage = MongoStorage(Config().mongo_host, 27017)

    async for x in SiteSpiegel().linked_articles(storage):
        if x.headline:
            logging.debug("---")
            logging.debug(f"{x.headline} @ {x.url}")
            logging.debug(f"{x.article_text}")
            logging.debug(str(x.text_sentiment))
            storage.store_article(x)


asyncio.run(main())
