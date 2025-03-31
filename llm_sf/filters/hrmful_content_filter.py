import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from better_profanity import profanity

nltk.download('vader_lexicon')

class HarmfulContentFilter:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.slur_keywords = profanity.load_censor_words()  # Możesz też podać własną listę
        self.mild_profanities = ["damn", "hell", "crap"]  # domyślnie – można nadpisać z buildera

    def check_severe_slurs(self, text, keywords=None):
        keywords = keywords or self.slur_keywords
        lower_text = text.lower()

        if profanity.contains_profanity(lower_text):
            return {
                "verdict": "block",
                "reason": "Detected severe harmful language",
                "final_text": text
            }

        return {
            "verdict": "allow",
            "reason": None,
            "final_text": text
        }

    def check_mild_profanity(self, text, profanities=None, replacement="[censored]"):
        profanities = profanities or self.mild_profanities
        lower_text = text.lower()
        sanitized = text

        hit = False
        for word in profanities:
            if word in lower_text:
                sanitized = re.sub(word, replacement, sanitized, flags=re.IGNORECASE)
                hit = True

        if hit:
            return {
                "verdict": "sanitize",
                "reason": "Mild profanity sanitized",
                "final_text": sanitized
            }

        return {
            "verdict": "allow",
            "reason": None,
            "final_text": text
        }

    def check_sentiment(self, text, threshold=-0.7):
        scores = self.analyzer.polarity_scores(text)
        if scores["compound"] < threshold:
            return {
                "verdict": "block",
                "reason": f"Negative sentiment below threshold {threshold}",
                "final_text": text
            }

        return {
            "verdict": "allow",
            "reason": None,
            "final_text": text
        }
