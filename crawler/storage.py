from abc import abstractmethod
from pymongo import MongoClient
from article import Article
import logging


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
        """Find an article by it's URL"""
        pass


class MongoStorage(ArticleStore):
    def __init__(self, hostname, port):
        logging.debug("Initialize mongo storage")
        self.mongo_client = MongoClient(host=hostname, port=port)
        self.mongo_db = self.mongo_client["testDB"]
        self.mongo_collection = self.mongo_db["articles"]

    def store_article(self, article):
        self.mongo_collection.insert_one(article.to_dict())

    def get_documents(self, fromdatetime=None, todatetime=None):
        query = {}

        time_constraints = {}
        if fromdatetime is not None:
            time_constraints["$gte"] = fromdatetime
        if todatetime is not None:
            time_constraints["$lte"] = todatetime

        if time_constraints != {}:
            query["fetch_time"] = time_constraints

        return list(self.mongo_collection.find(query))

    def article_by_url(self, url):
        return self.mongo_collection.find_one({ "url": url})
