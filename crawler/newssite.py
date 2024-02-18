import urllib
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timezone
from article import Article
import logging
import asyncio


async def get_soup_in(url):
    return BeautifulSoup(requests.get(url).text, "html.parser")


def links_in(soup):
    for a_tag in soup.find_all("a"):
        if a_tag.has_attr("href"):
            yield a_tag["href"]


class NewsSite:
    def __init__(self, site_domain):
        self.ignore_paywalled = True
        self.site_domain = site_domain
        self.backoff_seconds = 2

    async def parse_article_at_url(self, url):
        soup = await get_soup_in(url)
        headline = self.parse_headline(soup)
        article_text = self.parse_text(soup)

        if self.ignore_paywalled and self.is_paywalled(soup):
            return None

        article = await Article.new_article(
            url, headline, article_text, datetime.now(timezone.utc)
        )
        return article

    def parse_headline(self, soup):
        """Extract an article's headline"""
        for headline_tag in soup.find_all(["h1", "h2"]):
            return headline_tag.strings

    def parse_text(self, soup):
        """Get the text of an article"""
        paragraphs = []

        for p_tag in self.soup.find_all(["h1", "h2", "p"]):
            txt = " ".join(p_tag.strings).replace("\n", "")
            if len(txt) > 20:
                paragraphs.append(txt)

        return " ".join(paragraphs)

    def is_paywalled(self, soup):
        """True if the article is paywalled and we don't get the whole text"""
        return False

    def is_article_url(self, url):
        """Figure out if the given URL is a valid URL for an article that this
        parser expects

        """
        return True

    async def linked_articles(self, storage):
        visited_links = set()

        logging.debug(f"Crawling for articles on {self.site_domain}")

        for link in links_in(await get_soup_in(self.site_domain)):
            if urllib.parse.urlparse(link).scheme == "":
                continue

            if storage.article_by_url(link) is None:
                logging.debug(f"Ignoring article (already visited) {link}")
            elif not self.is_article_url(link):
                logging.debug(f"Ignoring non-article url: {link}")
            else:
                await asyncio.sleep(self.backoff_seconds)
                try:
                    article = await self.parse_article_at_url(link)
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


class SiteSpiegel(NewsSite):
    def __init__(self):
        super().__init__("https://www.spiegel.de")

    def parse_text(self, soup):
        return (
            " ".join(
                (
                    map(
                        lambda _: " ".join(_.strings),
                        list(
                            soup.find_all(
                                "div", {"data-sara-click-el": "body_element"})
                        ),
                    )
                )
            )
            .replace("\n", "")
            .strip()
        )

    def parse_headline(self, soup):
        try:
            return soup.select("header h2 .align-middle")[0].string
        except IndexError:
            return None

    def is_paywalled(self, soup):
        return soup.find("div", {"data-area": "paywall"}) is not None

    def is_article_url(self, url):
        return (
            len(
                list(
                    filter(
                        lambda x: x != "", urllib.parse.urlparse(
                            url).path.split("/")
                    )
                )
            )
            > 1
        )


class SiteZeit(NewsSite):
    def __init__(self):
        super().__init__("https://www.zeit.de")

    def parse_headline(self, soup):
        headline_tag = soup.find("span", class_="article-heading__title")
        return " ".join(headline_tag.strings)

    def parse_text(self, soup):
        article_body = soup.find("div", class_="article-body")
        if article_body is not None:
            paragraph_texts = map(
                lambda t: " ".join(t.strings),
                article_body.find_all("p", class_="paragraph"),
            )

            return " ".join(paragraph_texts).replace("\n", " ")

    def is_paywalled(self, soup):
        return soup.find("aside", id="paywall") is not None
