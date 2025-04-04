# profanity_filter.py
import re
from better_profanity import profanity
from .base_filter import BaseFilter, FilterResult

class ProfanityFilter(BaseFilter):
    """
    A filter responsible solely for detecting profanity using the 'better_profanity' library.

    This filter does not directly modify the final text in the system. Instead, it informs 
    whether the text should be blocked (`verdict='block'`) or sanitized (`verdict='sanitize'`) 
    based on configuration.
    """

    def __init__(
        self,
        custom_badwords=None,
        whitelist_words=None,
        block_on_detect=True,
        use_default_wordlist=True,
        censor_char='*'
    ):
        """
        Initializes the profanity filter with configurable wordlists and behavior.

        Args:
            custom_badwords (list, optional): A custom list of profane words to be loaded.
                If `use_default_wordlist` is False, this replaces the default list.
                If `use_default_wordlist` is True, these words will be added.
            whitelist_words (list, optional): A list of words that should not be treated as profanity.
            block_on_detect (bool): If True, detected profanity leads to a "block" verdict;
                otherwise, it results in "sanitize".
            use_default_wordlist (bool): If True, loads the default wordlist from the library.
            censor_char (str): Character(s) used by `.censor()` to replace profane words. Default is '*'.
        """
        self.block_on_detect = block_on_detect
        self.censor_char = censor_char

        # Load the wordlist depending on the configuration.
        # Note: better_profanity maintains a global state.
        if use_default_wordlist:
            profanity.load_censor_words(whitelist_words=whitelist_words)

            if custom_badwords:
                profanity.add_censor_words(custom_badwords)
        else:
            if custom_badwords is not None:
                profanity.load_censor_words(custom_badwords, whitelist_words=whitelist_words)
            else:
                profanity.load_censor_words([], whitelist_words=whitelist_words)

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
