import germansentiment

sentiment_model = germansentiment.SentimentModel()


class SentimentProbabilities:
    def __init__(self, positive, negative, neutral):
        self.positive = positive
        self.negative = negative
        self.neutral = neutral

    def __str__(self):
        return f"positive: {self.positive}, neutral: {self.neutral}, negative: {self.negative}"
