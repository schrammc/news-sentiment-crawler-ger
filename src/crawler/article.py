import crawler.sentiment
import dataclasses
from datetime import datetime


class Article:
    def __init__(self, url, headline, article_text, fetch_time, article_sentiment):
        self.url = url
        self.headline = headline
        self.article_text = article_text
        self.fetch_time = fetch_time
        self.text_sentiment = article_sentiment

    @classmethod
    async def new_article(cls, url, headline, article_text, fetch_time):
        article_sentiment = await crawler.sentiment.sentiment_of_text(article_text)
        return Article(url, headline, article_text, fetch_time, article_sentiment)

    def __str__(self):
        return f"{self.headline} | {self.text}"

    def to_dict(self):
        return {
            "url": self.url,
            "headline": self.headline,
            "article_text": self.article_text,
            "fetch_time": self.fetch_time,
            "text_sentiment": dataclasses.asdict(self.text_sentiment),
        }

    @classmethod
    def from_dict(cls, the_dict):
        fetch_time = None
        if type(the_dict["fetch_time"]).__name__ == "datetime":
            fetch_time = the_dict["fetch_time"]
        else:
            fetch_time = datetime.fromisoformat(the_dict["fetch_time"])

        return cls(
            the_dict["url"],
            the_dict["headline"],
            the_dict["article_text"],
            fetch_time,
            crawler.sentiment.SentimentProbabilities(**the_dict["text_sentiment"]),
        )
