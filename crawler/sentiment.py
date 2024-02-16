import germansentiment
from dataclasses import dataclass

sentiment_model = germansentiment.SentimentModel()


def sentiment_of_text(text):
    """Extract the sentiment of a piece of german text"""
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
