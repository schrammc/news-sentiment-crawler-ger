import requests
from bs4 import BeautifulSoup
import asyncio
import urllib
import logging

from parser import SpiegelParser, ZeitParser
from storage import MongoStorage

# General plan:
#   - Scrape news articles linked on front-page at any given time (do this once per hour?)
#   - Analyze for sentiment
#   - Provide API / UI

backoff_seconds_per_domain = 5

parsers = [ZeitParser(), SpiegelParser()]

storage = MongoStorage("localhost", 27017)


def get_soup_in(url):
    return BeautifulSoup(requests.get(url).text, "html.parser")


def links_in(soup):
    for a_tag in soup.find_all("a"):
        if a_tag.has_attr("href"):
            yield a_tag["href"]


async def linked_articles(parser):
    visited_links = set()
    homepage_url = parser.site_domain

    for link in links_in(get_soup_in(homepage_url)):
        if urllib.parse.urlparse(link).scheme == "":
            continue
        if link in visited_links:
            pass
        elif not parser.is_article_url(link):
            logging.debug(f"Ignoring non-article url: {link}")
        else:
            await asyncio.sleep(2)
            try:
                article = parser.parse_article_at_url(link)
                if (
                    article is not None
                    and article.headline is not None
                    and article.article_text is not None
                ):
                    logging.info(f"Parsed article: {article.url}")
                    yield article
            except requests.exceptions.HTTPError as err:
                logging.info(f"HTTPError: {err}")

        visited_links.add(link)


async def main():
    logging.info("Starting crawler")
    async for x in linked_articles(SpiegelParser()):
        if x.headline:
            logging.debug("---")
            logging.debug(f"{x.headline} @ {x.url}")
            logging.debug(f"{x.article_text}")
            logging.debug(str(x.text_sentiment))
            storage.store_article(x)


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] %(asctime)s -- %(message)s -- %(module)s:%(lineno)s",
)

asyncio.run(main())
