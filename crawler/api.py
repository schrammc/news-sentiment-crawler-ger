from fastapi import FastAPI
from storage import MongoStorage
from datetime import datetime
from appconfig import Config

config = Config()
storage = MongoStorage(config.mongo_host, 27017,
                       config.mongo_user, config.mongo_password)

app = FastAPI()


@app.get("/article")
def get_root(from_: datetime = None, to: datetime = None):
    docs = storage.get_documents(fromdatetime=from_, todatetime=to)
    for doc in docs:
        del doc["_id"]
        del doc["article_text"]
    return docs
