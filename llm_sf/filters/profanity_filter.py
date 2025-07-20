# profanity_filter.py
import csv
from better_profanity import profanity
from llm_sf.filters.base_filter import BaseFilter, FilterResult
from llm_sf.utils.constants import Constants

# the filter is a place to sanitization! not orchestrator
class ProfanityFilter(BaseFilter):


    def __init__(
        self,
        block_on_detect: bool = True, 
        weight: float = 1.0,
        custom_badwords = None,
        censor_char: str = '*'
    ):
        super().__init__(block_on_detect=block_on_detect, weight=weight)
  
        self.censor_char = censor_char
        self._load_profanities_from_csv()

        if custom_badwords:
            profanity.add_censor_words(custom_badwords)

    def run_filter(self, context) -> FilterResult:
        text = context.current_text

        if profanity.contains_profanity(text):
            risk_score = self.compute_risk_score(context)
            if self.block_on_detect:
                return FilterResult(
                    verdict=Constants.BLOCKED,
                    reason="Detected profanity. 'block_on_detect' is True.",
                    metadata={"risk_score": risk_score, "weight": self.weight}
                )
            else:
                sanitized_text = profanity.censor(text, self.censor_char)
                return FilterResult(
                    verdict=Constants.SANITIZED,
                    reason="Detected profanity. 'block_on_detect' is False -> sanitize suggested.",
                    metadata={
                        "sanitized_text": sanitized_text,
                        "risk_score": risk_score, 
                        "weight": self.weight    
                    }
                )

        return FilterResult(
            verdict=Constants.ALLOWED,
            reason="No profanity detected.",
            metadata={"risk_score": 0.0, "weight": self.weight}
        )

    def compute_risk_score(self, context) -> float:
        text = context.current_text

        if not profanity.contains_profanity(text):
            return 0.0

        censored_text = profanity.censor(text, self.censor_char)

        original_words = text.split()
        censored_words = censored_text.split()

        # Count how many words were censored (contain censor_char)
        num_censored_words = sum(
            1 for orig, censored in zip(original_words, censored_words)
            if self.censor_char in censored and orig != censored
        )

        total_words = len(original_words)

        result = round(min(num_censored_words / total_words, 1.0), 1)
        print("num_censored_words:", num_censored_words)
        print("total_words:", total_words)
        print("risk_score:", result)
        return result

    def _load_profanities_from_csv(self):
        try:
            with open(Constants.PROFANITIES_CSV, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                csv_badwords = [row[0].strip() for row in reader if row]
                profanity.add_censor_words(csv_badwords)
        except Exception as e:
            print(f"Warning: Failed to load profanity words from CSV: {e}")