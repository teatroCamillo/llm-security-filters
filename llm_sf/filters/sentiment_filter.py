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
    """
    A filter that detects and reacts to negative sentiment in text.

    Uses NLTK's VADER sentiment analysis tool to evaluate input content. 
    If the compound sentiment score falls below a specified threshold,
    the text may be blocked or flagged for sanitization.
    """

    def __init__(
        self,
        block_on_detect: bool = True, 
        weight: float = 1.0, 
        threshold=-0.7
        ):
        super().__init__(block_on_detect=block_on_detect, weight=weight)
        """
        Initializes the sentiment filter with configuration options.

        Args:
            threshold (float): Minimum acceptable compound sentiment score. Below this value, the text is flagged.
            block_on_detect (bool): Determines whether to block or sanitize when sentiment is too negative.
        """
        self.threshold = threshold
        self.analyzer = SentimentIntensityAnalyzer()
        self.profanites = self._load_profanities_from_csv()
        
        for word in self.profanites:
            self._updadte_lexicon(word, -4.0)

    def run_filter(self, context) -> FilterResult:
        """
        Analyzes the sentiment of the input text and returns a filtering decision.

        If the compound sentiment score is below the configured threshold, the filter 
        either blocks or sanitizes the text depending on the `block_on_detect` setting.

        Args:
            context: The Context object containing the text to analyze.

        Returns:
            FilterResult: The result of the sentiment analysis, indicating whether 
                          the text is allowed, blocked, or needs sanitization.
        """

        '''
        PROBLEMS or It shoudl work like this:
        blowjob,You're amazing when you give me a blowjob. - because amazing is positive
        fuck,I love fuck you in that way. - cuz love is positive
        '''

        text = context.current_text
        text = self.add_whitespace_around_punctuation(text)
        print(f"Analyzing sentiment for text: {text}")
        scores = self.analyzer.polarity_scores(text)

        risk_score = self.compute_risk_score(scores["compound"])
        print(f"scores[compound]: ", scores["compound"])
        print(f"risk_score: {risk_score}")

        if scores["compound"] < self.threshold:
            verdict = Constants.BLOCKED if self.block_on_detect else Constants.SANITIZED
            return FilterResult(
                verdict=verdict,
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
        """
        Updates the sentiment lexicon with a new word and its score.

        Args:
            word (str): The word to add to the lexicon.
            score (float): The sentiment score for the word. Range from -4.0 to 4.0.
        """
        self.analyzer.lexicon[word] = score
        #print(f"Updated lexicon: {word} -> {score}")

    def add_whitespace_around_punctuation(self, text):
        #pattern = f'([{re.escape("!?,.:;\"\'()[]{}<>")}]])'
        pattern = f'([{re.escape("!?,.:;")}])'
        return re.sub(pattern, r' \1 ', text)
    
    def compute_risk_score(self, score_compound) -> float:
        # Normalize: map [-1.0, 0) → [1.0, 0.0]
        risk_score = round((1 - score_compound) / 2, 2)

        print("compound:", score_compound)
        print("risk_score:", risk_score)
        return risk_score

    def _load_profanities_from_csv(self):
        """
        Loads the first column of profanity words from the configured CSV file and adds them
        to the profanity filter.
        """
        try:
            with open(Constants.MUTATED_WORDS_CSV, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                csv_badwords = [row[1].strip() for row in reader if row]
                
                # target_word = "blowjob"
                # is_badword = target_word in csv_badwords
                # print(f"Is '{target_word}' a bad word? {is_badword}")
        except Exception as e:
            print(f"Warning: Failed to load profanity words from CSV: {e}")

        # for word in range(55,70):
        #     print(f"Adding word: {csv_badwords[word]}")
        return csv_badwords