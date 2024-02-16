import requests
from bs4 import BeautifulSoup
import asyncio
import urllib
import logging
from parser import SpiegelParser, ZeitParser

# General plan:
#   - Scrape news articles linked on front-page at any given time (do this once per hour?)
#   - Analyze for sentiment
#   - Provide API / UI

backoff_seconds_per_domain = 5

parsers = [ZeitParser(), SpiegelParser()]


def get_soup_in(url):
    return BeautifulSoup(requests.get(url).text, "html.parser")


def links_in(soup):
    for a_tag in soup.find_all("a"):
        if a_tag.has_attr("href"):
            yield a_tag["href"]


async def linked_articles(homepage_url, parser):
    visited_links = set()

    for link in links_in(get_soup_in(homepage_url)):
        if urllib.parse.urlparse(link).scheme == "":
            continue
        print(link)
        if link not in visited_links and parser.is_article_url(link):
            await asyncio.sleep(2)
            try:
                yield (parser.parse_article(link))
            except requests.exceptions.HTTPError as err:
                logging.info(f"HTTPError: {err}")

        visited_links.add(link)


async def main():
    logging.info("Starting crawler")
    async for x in linked_articles("https://www.spiegel.de", SpiegelParser()):
        if x.headline:
            logging.debug("---")
            logging.debug(f"{x.headline} @ {x.url}")
            logging.debug(f"{x.text}")
            logging.debug(str(x.text_sentiment()))


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] %(asctime)s -- %(message)s -- %(module)s:%(lineno)s",
)

asyncio.run(main())
