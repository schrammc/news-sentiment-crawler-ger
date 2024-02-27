import germansentiment
from dataclasses import dataclass
import logging
import asyncio

sentiment_model = None
sentiment_model_lock = asyncio.Lock()


async def get_sentiment_model():
    """Retrieve the global sentiment model."""
    global sentiment_model
    async with sentiment_model_lock:
        if sentiment_model is None:
            logging.info("Building sentiment model...")
            sentiment_model = germansentiment.SentimentModel()

    return sentiment_model


async def sentiment_of_text(text):
    """Extract the sentiment of a piece of german text."""
    sentiment_model = await get_sentiment_model()

    probs = sentiment_model.predict_sentiment(
        [text],
        output_probabilities=True,
    )

    return SentimentProbabilities(
        probs[1][0][0][1], probs[1][0][1][1], probs[1][0][2][1]
    )


@dataclass
class SentimentProbabilities:
    positive: float
    negative: float
    neutral: float

    def __str__(self):
        return f"positive: {self.positive}, neutral: {self.neutral}, negative: {self.negative}"
