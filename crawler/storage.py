from abc import abstractmethod
from pymongo import MongoClient
from crawler.parser import Article


class ArticleStore:
    @abstractmethod
    def store_article(self, article):
        pass

    @abstractmethod
    def get_all_documents(self):
        pass


class MongoStorage(ArticleStore):
    def __init__(self, hostname, port):
        self.mongo_client = MongoClient(host=hostname, port=port)
        self.mongo_db = self.mongo_client["testDB"]
        self.mongo_collection = self.mongo_db["articles"]

    def store_article(self, article):
        self.mongo_collection.insert_one(article.to_dict())

    def get_all_documents(self):
        for document in self.mongo_collection.find({}):
            print(str(Article.from_dict(document)))
