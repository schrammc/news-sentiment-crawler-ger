import germansentiment
from dataclasses import dataclass
import logging

sentiment_model = None


def get_sentiment_model():
    global sentiment_model
    logging.info("Building sentiment model...")
    if sentiment_model is None:
        sentiment_model = germansentiment.SentimentModel()

    return sentiment_model


def sentiment_of_text(text):
    """Extract the sentiment of a piece of german text"""
    probs = get_sentiment_model().predict_sentiment(
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
