from fastapi import FastAPI
from storage import MongoStorage

storage = MongoStorage("localhost", 27017)

app = FastAPI()


@app.get("/article")
def get_root(from_: datetime = None, to: datetime = None):
    docs = storage.get_documents(fromdatetime=from_, todatetime=to)
    for doc in docs:
        del doc["_id"]
        del doc["article_text"]
    return docs