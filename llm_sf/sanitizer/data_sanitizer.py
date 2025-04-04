# data_sanitizer.py
from typing import List
from llm_sf.filters.base_filter import FilterResult

class DataSanitizer:
    """
    Provides final sanitization logic for input text based on filter results.

    Combines sanitization suggestions from multiple filters into a unified
    version of the text. Useful in both serial and parallel filtering scenarios.
    """

    def sanitize(self, original_text: str, filters_results: List[FilterResult]) -> str:
        """
        Returns the final sanitized version of the text based on filter metadata.

        Iterates over all filters that suggested sanitization and applies their
        sanitized versions sequentially.

        Args:
            original_text (str): The original, unmodified input text.
            filters_results (List[FilterResult]): A list of results returned by filters,
                typically in serial or parallel execution mode.

        Returns:
            str: The final version of the text after all suggested sanitizations.
        """
        sanitized_text = original_text

        for result in filters_results:
            if result.verdict == "sanitize":
                possible_sanitized = result.metadata.get("sanitized_text")
                if possible_sanitized:
                    sanitized_text = self._combine_sanitizations(
                        base_text=sanitized_text,
                        new_sanitized=possible_sanitized,
                        original_text=original_text
                    )

        return sanitized_text

    def _combine_sanitizations(self, base_text: str, new_sanitized: str, original_text: str) -> str:
        """
        Merges a newly suggested sanitized version into the current base version.

        Assumes both sanitized versions are based on the same original input.
        The default implementation simply adopts the latest sanitized version.

        Args:
            base_text (str): The currently accumulated sanitized version.
            new_sanitized (str): A new suggestion for a sanitized version from a filter.
            original_text (str): The original unmodified input text.

        Returns:
            str: The updated sanitized version of the text.
        """
        return new_sanitized
