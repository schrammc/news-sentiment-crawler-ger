import requests
from bs4 import BeautifulSoup
import germansentiment
import asyncio
import urllib
import hashlib

# General plan:
#   - Scrape news articles linked on front-page at any given time (do this once per hour?)
#   - Analyze for sentiment
#   - Provide API / UI

sentiment_model = germansentiment.SentimentModel()

backoff_seconds_per_domain = 5

top_domains = ["www.zeit.de", "www.spiegel.de", "www.fr.de"]


def get_soup_in(url):
    return BeautifulSoup(requests.get(url).text, "html.parser")


def links_in(soup):
    for a_tag in soup.find_all("a"):
        if a_tag.has_attr("href"):
            yield a_tag["href"]


def text_in(soup):
    paragraphs = []

    for p_tag in soup.find_all(["h1", "h2", "p"]):
        txt = " ".join(p_tag.strings).replace("\n", "")
        if len(txt) > 20:
            paragraphs.append(txt)

    return " ".join(paragraphs)


class SentimentProbabilities:
    def __init__(self, positive, negative, neutral):
        self.positive = positive
        self.negative = negative
        self.neutral = neutral

    def __str__(self):
        return f"positive: {self.positive}, neutral: {self.neutral}, negative: {self.negative}"


class Article:
    def __init__(self, url, text):
        self.url = url
        self.soup = BeautifulSoup(text, "html.parser")
        self.text = text_in(self.soup)

    @classmethod
    def from_url(class_, url):
        article_text = requests.get(url).text
        return class_(url, article_text)

    def text_sentiment(self):
        probs = sentiment_model.predict_sentiment(
            [text_in(self.soup)],
            output_probabilities=True,
        )

        return SentimentProbabilities(
            probs[1][0][0][1], probs[1][0][1][1], probs[1][0][2][1]
        )


async def linked_articles(url):
    visited_links = set()

    for link in links_in(get_soup_in(url)):
        if urllib.parse.urlparse(link).scheme == "":
            continue

        if not link in visited_links:
            await asyncio.sleep(2)
            try:
                yield (Article.from_url(link))
            except:
                pass

        visited_links.add(link)


async def main():
    async for x in linked_articles("https://www.spiegel.de"):
        print("---")
        print(x.url)
        print(str(x.text_sentiment()))


asyncio.run(main())
