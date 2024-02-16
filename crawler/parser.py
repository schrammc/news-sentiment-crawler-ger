import urllib
from bs4 import BeautifulSoup
from sentiment import SentimentProbabilities, sentiment_model
import requests
from dataclasses import dataclass


@dataclass  # noqa: F821
class Article:
    url: str
    headline: str | None
    article_text: str | None

    def text_sentiment(self):
        """Extract the sentiment of an article's text"""
        probs = sentiment_model.predict_sentiment(
            [self.article_text],
            output_probabilities=True,
        )

        return SentimentProbabilities(
            probs[1][0][0][1], probs[1][0][1][1], probs[1][0][2][1]
        )

    def __str__(self):
        return f"{self.headline} | {self.text}"


class ArticleParser:
    def __init__(self, site_domain):
        self.ignore_paywalled = True
        self.site_domain = site_domain

    def parse_article_at_url(self, url):
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        headline = self.parse_headline(soup)
        article_text = self.parse_text(soup)

        if self.ignore_paywalled and self.is_paywalled(soup):
            return None

        return Article(url, headline, article_text)

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
        """Figure out if the given URL is a valid URL for an article that this parser expects"""
        return True


class SpiegelParser(ArticleParser):
    def __init__(self):
        super().__init__("www.spiegel.de")

    def parse_text(self, soup):
        return (
            " ".join(
                (
                    map(
                        lambda _: " ".join(_.strings),
                        list(
                            soup.find_all("div", {"data-sara-click-el": "body_element"})
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
                        lambda x: x != "", urllib.parse.urlparse(url).path.split("/")
                    )
                )
            )
            > 1
        )


class ZeitParser(ArticleParser):
    def __init__(self):
        super().__init__("www.zeit.de")

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
