import logging
import sys
import asyncio
from appconfig import Config

from newssite import NewsSite, SiteSpiegel, SiteZeit
from storage import ArticleStore, MongoStorage

sites = [SiteSpiegel(), SiteZeit()]


async def crawl_and_store(storage: ArticleStore, site: NewsSite, loop_delay_minutes: int = 10):
    """Crawl the articles from the given site forever.

    :param loop_delay_minutes: the amount wait-time before crawling again"""
    while True:
        try:
            async for x in site.linked_articles(storage):
                if x.headline:
                    logging.debug(f"Storing article {x.headline} @ {x.url}")
                    storage.store_article(x)

            logging.debug(
                f"Sleeping {loop_delay_minutes} minutes before looping")
        except Exception as e:
            logging.error(f"Exception while crawling {site.site_domain}: {e}")
        finally:
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
