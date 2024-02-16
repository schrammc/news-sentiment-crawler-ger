from fastapi import FastAPI
from storage import MongoStorage

storage = MongoStorage("localhost", 27017)

app = FastAPI()


@app.get("/article")
def get_root():
    docs = storage.get_all_documents()
    for doc in docs:
        del doc["_id"]
    return docs
