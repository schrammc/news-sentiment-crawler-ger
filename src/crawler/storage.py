from abc import abstractmethod
from pymongo import MongoClient
from crawler.article import Article
from statistics import mean
import logging
from crawler.sentiment import SentimentProbabilities


class ArticleStore:
    @abstractmethod
    def store_article(self, article):
        pass

    @abstractmethod
    def get_documents(self, fromdatetime=None, todatetime=None):
        """Get documents possibly limited by time

        :param fromdatetime: If this is given, select only articles from on or after this time
        :param todatetime: If this is given, select only articles from on or before this time
        """
        pass

    @abstractmethod
    def article_by_url(self, url):
        """Find an article by it's URL."""
        pass

    @abstractmethod
    def avg_sentiment_by_day(self, fromdatetime=None, todatetime=None):
        """Get average sentiments for each day."""
        pass


class MongoStorage(ArticleStore):
    def __init__(self, hostname, port, username=None, password=None):
        logging.debug("Initialize mongo storage")
        self.mongo_client = MongoClient(
            host=hostname, port=port, username=username, password=password)
        self.mongo_db = self.mongo_client["testDB"]
        self.mongo_collection = self.mongo_db["articles"]

    def store_article(self, article):
        self.mongo_collection.insert_one(article.to_dict())

    def make_article_query(self, fromdatetime, todatetime):
        query = {}

        time_constraints = {}
        if fromdatetime is not None:
            time_constraints["$gte"] = fromdatetime
        if todatetime is not None:
            time_constraints["$lte"] = todatetime

        if time_constraints != {}:
            query["fetch_time"] = time_constraints

        return query

    def get_documents(self, fromdatetime=None, todatetime=None):
        return list(self.mongo_collection.find(self.make_article_query(fromdatetime, todatetime)))

    def avg_sentiment_by_day(self):
        arts_by_date = {}
        for doc in self.mongo_collection.find({}):
            article = Article.from_dict(doc)
            article_date = article.fetch_time.date()
            if article_date in arts_by_date:
                arts_by_date[article_date].append(article)
            else:
                arts_by_date[article_date] = [article]

        avg_sentiments = {}
        for date in arts_by_date:
            (positive, negative, neutral) = zip(*map(lambda x: [x.text_sentiment.positive,
                                                               x.text_sentiment.negative,
                                                               x.text_sentiment.neutral
                                                               ], arts_by_date[date]))
            avg_sentiments[date] = SentimentProbabilities(mean(positive),
                                                          mean(negative),
                                                          mean(neutral)
                                                          )

        return avg_sentiments

    def article_by_url(self, url):
        return self.mongo_collection.find_one({"url": url})
