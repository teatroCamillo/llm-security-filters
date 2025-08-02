# sentiment_filter.py
import nltk
import csv
import re
import string
from nltk.sentiment import SentimentIntensityAnalyzer
from llm_sf.filters.base_filter import BaseFilter
from llm_sf.filter_manager.filter_result import FilterResult
from llm_sf.utils.constants import Constants
from llm_sf.utils.word_mutator import WordMutator

# Downloading the sentiment lexicon required by VADER
nltk.download('vader_lexicon', quiet=True)

class SentimentFilter(BaseFilter):

    def __init__(
        self,
        weight: float = 1.0, 
        threshold=-0.5
        ):
        super().__init__(weight=weight)
        self.threshold = threshold
        self.analyzer = SentimentIntensityAnalyzer()
        
        for word in Constants.load_csv(Constants.PROFANITIES_FULL_CSV):
            self._update_lexicon(word, -4.0)
        
        for word in Constants.load_csv(Constants.HIGH_RISK_WORDS_CSV):
            self._update_lexicon(word, -4.0)

    def run_filter(self, context) -> FilterResult:
        text = context.current_text
        text = self.add_whitespace_around_punctuation(text)
        scores = self.analyzer.polarity_scores(text)
        risk_score = self.compute_risk_score(scores["compound"])

        if scores["compound"] < self.threshold:
            return FilterResult(
                verdict=Constants.BLOCKED,
                reason=f"Negative sentiment {scores['compound']} below threshold {self.threshold}",
                metadata = {
                    "original_text": context.original_text,
                    "sentiment_scores": scores,
                    "risk_score": risk_score,
                    "weight": self.weight
                }
            )
        else:
            return FilterResult(
                verdict=Constants.ALLOWED,
                reason=f"No negative sentiment detected: {scores['compound']} above threshold {self.threshold}",
                metadata = {
                    "original_text": context.original_text,
                    "sentiment_scores": scores,
                    "risk_score": risk_score,
                    "weight": self.weight
                }
            )

    def _update_lexicon(self, word, score):
        self.analyzer.lexicon[word] = score

    def add_whitespace_around_punctuation(self, text):
        pattern = f'([{re.escape("!?,.:;")}])'
        return re.sub(pattern, r' \1 ', text)
    
    def compute_risk_score(self, score_compound) -> float:
        return round((1 - score_compound) / 2, 2)
