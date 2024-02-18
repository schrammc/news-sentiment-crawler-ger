from abc import abstractmethod
from pymongo import MongoClient
from parser import Article

class ArticleStore:
    @abstractmethod
    def store_article(self, article):
        pass

    @abstractmethod
    def get_documents(self, fromdatetime=None, todatetime=None):
        pass


class MongoStorage(ArticleStore):
    def __init__(self, hostname, port):
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
