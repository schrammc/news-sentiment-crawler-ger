import sentiment
import dataclasses


class Article:
    def __init__(self, url, headline, article_text, fetch_time, article_sentiment):
        self.url = url
        self.headline = headline
        self.article_text = article_text
        self.fetch_time = fetch_time
        self.text_sentiment = article_sentiment

    @classmethod
    async def new_article(cls, url, headline, article_text, fetch_time):
        article_sentiment = await sentiment.sentiment_of_text(article_text)
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
        cls(
            the_dict["url"],
            the_dict["headline"],
            the_dict["article_text"],
            the_dict["fetch_time"],
            sentiment.SentimentProbabilities(**the_dict["text_sentiment"]),
        )
