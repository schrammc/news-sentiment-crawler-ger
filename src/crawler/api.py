from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crawler.storage import MongoStorage
from datetime import datetime
from crawler.appconfig import Config
from crawler.sentiment import SentimentProbabilities
import uvicorn

config = Config()
storage = MongoStorage(config.mongo_host, 27017,
                       config.mongo_user, config.mongo_password)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://christof-schramm.net"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
    )

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
    result = {}

    for date, sentiment in storage.avg_sentiment_by_day().items():
        result[date.isoformat()] = sentiment

    return result

def start():
    uvicorn.run("crawler.api:app", host="0.0.0.0", port=8080)
