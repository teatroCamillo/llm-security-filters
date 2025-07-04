# profanity_filter.py
import csv
from better_profanity import profanity
from llm_sf.filters.base_filter import BaseFilter, FilterResult
from llm_sf.utils.constants import Constants
# the filter is a place to sanitization! not orchestrator
class ProfanityFilter(BaseFilter):
    """
    A filter responsible solely for detecting profanity using the 'better_profanity' library.

    This filter does not directly modify the final text in the system. Instead, it informs 
    whether the text should be blocked (`verdict='block'`) or sanitized (`verdict='sanitize'`) 
    based on configuration.
    """

    def __init__(
        self,
        block_on_detect: bool = True, 
        weight: float = 1.0,
        custom_badwords = None,
        censor_char: str = '*'
    ):
        super().__init__(block_on_detect=block_on_detect, weight=weight)
        """
        Initializes the profanity filter with configurable wordlists and behavior.
        """
        self.censor_char = censor_char
        self._load_profanities_from_csv()

        if custom_badwords:
            profanity.add_censor_words(custom_badwords)

    def run_filter(self, context) -> FilterResult:
        """
        Applies the profanity filter to the provided context text.

        Depending on the configuration, detected profanity leads to either a "block" or "sanitize" verdict.
        Sanitized text is included in metadata if applicable.

        Args:
            context: An object containing the current text under `context.current_text`.

        Returns:
            FilterResult: The result of the filtering operation, which can be:
                - "block" if profanity is detected and blocking is enabled,
                - "sanitize" if profanity is detected and blocking is disabled,
                - "allow" if no profanity is found.
        """
        text = context.current_text

        if profanity.contains_profanity(text):
            if self.block_on_detect:
                return FilterResult(
                    verdict="block",
                    reason="Detected profanity. 'block_on_detect' is True."
                )
            else:
                sanitized_text = profanity.censor(text, self.censor_char)
                return FilterResult(
                    verdict="sanitize",
                    reason="Detected profanity. 'block_on_detect' is False -> sanitize suggested.",
                    metadata={"sanitized_text": sanitized_text}
                )

        return FilterResult(
            verdict="allow",
            reason="No profanity detected."
        )

    def _load_profanities_from_csv(self):
        """
        Loads the first column of profanity words from the configured CSV file and adds them
        to the profanity filter.
        """
        try:
            with open(Constants.PROFANITIES_CSV, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                csv_badwords = [row[0].strip() for row in reader if row]
                profanity.add_censor_words(csv_badwords)
        except Exception as e:
            print(f"Warning: Failed to load profanity words from CSV: {e}")