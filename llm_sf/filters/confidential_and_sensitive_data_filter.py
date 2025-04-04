# confidential_and_sensitive_data_filter.py
import re
from llm_sf.filters.base_filter import BaseFilter, FilterResult

class ConfidentialAndSensitiveDataFilter(BaseFilter):
    """
    A filter for detecting confidential or sensitive information in text.

    Detects data such as phone numbers, email addresses, and credit card numbers.
    Depending on configuration, the filter may either block such content or suggest
    sanitization by redacting the sensitive parts.
    """

    def __init__(self, block_on_detect: bool = False):
        """
        Initializes the filter with an optional blocking behavior.

        Args:
            block_on_detect (bool): If True, any detected sensitive data results in 'block'.
                                    If False, the filter returns 'sanitize' with redacted text.
        """
        self.block_on_detect = block_on_detect

        # Regular expressions for detecting common types of sensitive data.
        self.patterns = {
            "PHONE": re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"),
            "EMAIL": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
            "CREDIT_CARD": re.compile(r"\b(?:\d[ -]*?){13,16}\b")
        }

    def run_filter(self, context):
        """
        Scans the input text for sensitive information and returns an appropriate verdict.

        If any sensitive patterns are detected (e.g., email, phone, credit card), the result
        is either 'block' or 'sanitize', depending on the configuration. Sanitized output replaces
        sensitive data with placeholders like [EMAIL], [PHONE], etc.

        Args:
            context: The Context object containing the current text to evaluate.

        Returns:
            FilterResult: A result indicating whether the text is allowed, needs sanitization, or should be blocked.
        """
        text = context.current_text
        found_sensitive_data = False

        # Check if any sensitive data pattern matches the text.
        for name, pattern in self.patterns.items():
            if pattern.search(text):
                found_sensitive_data = True
                break

        if found_sensitive_data:
            if self.block_on_detect:
                return FilterResult(
                    verdict="block",
                    reason="Detected confidential/sensitive data. 'block_on_detect' is True."
                )
            else:
                # Replace sensitive data with placeholders for sanitization.
                sanitized_text = text
                for name, pattern in self.patterns.items():
                    placeholder = f"[{name}]"
                    sanitized_text = pattern.sub(placeholder, sanitized_text)

                return FilterResult(
                    verdict="sanitize",
                    reason="Detected confidential/sensitive data. Suggesting sanitization.",
                    metadata={"sanitized_text": sanitized_text}
                )

        return FilterResult(
            verdict="allow",
            reason="No confidential/sensitive data detected."
        )
