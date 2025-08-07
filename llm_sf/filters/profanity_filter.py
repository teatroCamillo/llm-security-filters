# profanity_filter.py
import csv
import re
import math
from better_profanity import profanity
from llm_sf.filters.base_filter import BaseFilter, FilterResult
from llm_sf.filter_manager.filter_result import FilterResult
from llm_sf.utils.constants import Constants

class ProfanityFilter(BaseFilter):

    def __init__(
        self,
        weight: float = 1.0,
        custom_badwords = None
    ):
        super().__init__(weight=weight)
        profanity.add_censor_words(Constants.load_csv(Constants.PROFANITIES_FULL_CSV))
        
        if custom_badwords:
            profanity.add_censor_words(custom_badwords)

    def run_filter(self, context) -> FilterResult:
        text = re.sub(r"[\'\.\?]", '', context.current_text)

        if profanity.contains_profanity(text):
            risk_score = self.compute_risk_score(context)
            return FilterResult(
                verdict=Constants.BLOCKED,
                reason="Detected profanity.",
                metadata={"original_text": context.original_text, "risk_score": risk_score, "weight": self.weight}
            )

        return FilterResult(
            verdict=Constants.ALLOWED,
            reason="No profanity detected.",
            metadata={"original_text": context.original_text, "risk_score": 0.0, "weight": self.weight}
        )

    def compute_risk_score(self, context) -> float:
        text = context.current_text

        if not profanity.contains_profanity(text):
            return 0.0

        censored_text = profanity.censor(text, "*")
        original_words = text.split()
        censored_words = censored_text.split()

        num_censored_words = sum(
            1 for orig, censored in zip(original_words, censored_words)
            if censor_char in censored and orig != censored
        )

        total_words = len(original_words)
        if total_words == 0:
            return 0.0

        proportion = num_censored_words / total_words
        raw_score = num_censored_words / (math.log(total_words + 1) + 1)
        normalized_score = min(raw_score, 1.0)
        return round(normalized_score, 2)