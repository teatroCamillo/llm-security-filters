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
        threshold=-0.7
        ):
        super().__init__(weight=weight)

        self.threshold = threshold
        self.analyzer = SentimentIntensityAnalyzer()
        self.profanites = self._load_profanities_from_csv()
        
        for word in self.profanites:
            self._updadte_lexicon(word, -4.0)

    def run_filter(self, context) -> FilterResult:

        text = context.current_text
        text = self.add_whitespace_around_punctuation(text)
        print(f"Analyzing sentiment for text: {text}")
        scores = self.analyzer.polarity_scores(text)

        risk_score = self.compute_risk_score(scores["compound"])
        print(f"scores[compound]: ", scores["compound"])
        print(f"risk_score: {risk_score}")

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
                metadata = {
                    "original_text": context.original_text,
                    "sentiment_scores": scores,
                    "risk_score": risk_score,
                    "weight": self.weight
                }
            )

    def _updadte_lexicon(self, word, score):
        self.analyzer.lexicon[word] = score
        #print(f"Updated lexicon: {word} -> {score}")

    def add_whitespace_around_punctuation(self, text):
        #pattern = f'([{re.escape("!?,.:;\"\'()[]{}<>")}]])'
        pattern = f'([{re.escape("!?,.:;")}])'
        return re.sub(pattern, r' \1 ', text)
    
    def compute_risk_score(self, score_compound) -> float:
        risk_score = round((1 - score_compound) / 2, 2)

        # print("compound:", score_compound)
        # print("risk_score:", risk_score)
        return risk_score

    def _load_profanities_from_csv(self):

        try:
            with open(Constants.MUTATED_WORDS_CSV, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                csv_badwords = [row[1].strip() for row in reader if row]
                
                # target_word = "blowjob"
                # is_badword = target_word in csv_badwords
                # print(f"Is '{target_word}' a bad word? {is_badword}")
        except Exception as e:
            print(f"Warning: Failed to load profanity words from CSV: {e}")

        return csv_badwords