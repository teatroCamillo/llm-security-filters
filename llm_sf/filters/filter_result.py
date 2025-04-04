# filter_result.py
from typing import Dict, Any

class FilterResult:
    """
    Represents the result of a content filtering operation.

    Stores the decision made by a filter (e.g., allow, block, sanitize), along with
    an optional reason and metadata for further context or downstream processing.
    """

    def __init__(self, verdict: str, reason: str = None, metadata: Dict[str, Any] = None):
        """
        Initializes a FilterResult instance.

        Args:
            verdict (str): The outcome of the filtering process. Valid values are 'allow', 'block', or 'sanitize'.
            reason (str, optional): An explanation or justification for the filtering decision.
            metadata (Dict[str, Any], optional): Additional data relevant to the result, such as sanitized text.
        """
        self.verdict = verdict
        self.reason = reason
        self.metadata = metadata or {}

    def __repr__(self):
        """
        Returns a string representation of the FilterResult object.

        Useful for debugging and logging purposes.

        Returns:
            str: A string describing the FilterResult instance.
        """
        return f"FilterResult(verdict={self.verdict}, reason={self.reason}, metadata={self.metadata})"
