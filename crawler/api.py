from fastapi import FastAPI
from storage import MongoStorage
from datetime import datetime
from appconfig import Config
from sentiment import SentimentProbabilities

config = Config()
storage = MongoStorage(config.mongo_host, 27017,
                       config.mongo_user, config.mongo_password)

app = FastAPI()


@app.get("/article")
def get_root(from_: datetime = None, to: datetime = None):
    """Get all articles."""
    docs = storage.get_documents(fromdatetime=from_, todatetime=to)
    for doc in docs:
        del doc["_id"]
        del doc["article_text"]
    return docs


@app.get("/sentiment")
def get_sentiments() -> dict[datetime, SentimentProbabilities]:
    """Get aggregated article sentiment information by day.

    Note that the invariant that sentiment probabilities add up to 1 does not
    hold for this output. The values are just the respective arithmetic means
    of positive/negative/neutral

    """
    return storage.avg_sentiment_by_day()
