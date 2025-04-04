# sentiment_filter.py
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from filters.base_filter import BaseFilter, FilterResult

# Downloading the sentiment lexicon required by VADER
nltk.download('vader_lexicon', quiet=True)

class SentimentFilter(BaseFilter):
    """
    A filter that detects and reacts to negative sentiment in text.

    Uses NLTK's VADER sentiment analysis tool to evaluate input content. 
    If the compound sentiment score falls below a specified threshold,
    the text may be blocked or flagged for sanitization.
    """

    def __init__(self, threshold=-0.7, block_on_negative=True):
        """
        Initializes the sentiment filter with configuration options.

        Args:
            threshold (float): Minimum acceptable compound sentiment score. Below this value, the text is flagged.
            block_on_negative (bool): Determines whether to block or sanitize when sentiment is too negative.
        """
        self.threshold = threshold
        self.block_on_negative = block_on_negative
        self.analyzer = SentimentIntensityAnalyzer()

    def run_filter(self, context) -> FilterResult:
        """
        Analyzes the sentiment of the input text and returns a filtering decision.

        If the compound sentiment score is below the configured threshold, the filter 
        either blocks or sanitizes the text depending on the `block_on_negative` setting.

        Args:
            context: The Context object containing the text to analyze.

        Returns:
            FilterResult: The result of the sentiment analysis, indicating whether 
                          the text is allowed, blocked, or needs sanitization.
        """
        text = context.current_text
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
