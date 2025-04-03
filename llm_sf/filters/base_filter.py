from typing import Dict, Any

class FilterResult:
    def __init__(self, verdict: str, reason: str = None, metadata: Dict[str, Any] = None):
        self.verdict = verdict  # "allow" | "block" | "sanitize" 
        self.reason = reason
        self.metadata = metadata or {}

    def __repr__(self):
        return f"FilterResult(verdict={self.verdict}, reason={self.reason}, metadata={self.metadata})"


class BaseFilter:
    """
    Klasa bazowa dla wszystkich filtrów. 
    Każdy filtr powinien implementować metodę run_filter(context), 
    która zwraca obiekt FilterResult.
    """
    def run_filter(self, context) -> FilterResult:
        raise NotImplementedError("Must implement run_filter() in subclass")
