import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from .base_filter import BaseFilter, FilterResult

# to samo – załadowanie leksykonu
nltk.download('vader_lexicon', quiet=True)

class SentimentFilter(BaseFilter):
    """
    Filtr odpowiedzialny tylko za wykrywanie niewłaściwego sentymentu
    (np. bardzo niska wartość compound).
    """

    def __init__(self, threshold=-0.7, block_on_negative=True):
        self.threshold = threshold
        self.block_on_negative = block_on_negative
        self.analyzer = SentimentIntensityAnalyzer()

    def run_filter(self, context) -> FilterResult:
        text = context.original_text
        scores = self.analyzer.polarity_scores(text)
        
        if scores["compound"] < self.threshold:
            verdict = "block" if self.block_on_negative else "sanitize"
            return FilterResult(
                verdict=verdict,
                reason=f"Negative sentiment {scores['compound']} below threshold {self.threshold}",
                metadata={"sentiment_scores": scores}
            )
        else:
            return FilterResult(
                verdict="allow",
                metadata={"sentiment_scores": scores}
            )
