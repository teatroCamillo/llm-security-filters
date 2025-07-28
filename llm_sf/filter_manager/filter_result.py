# filter_result.py
from typing import Dict, Any

class FilterResult:

    def __init__(self, verdict: str, reason: str = None, metadata: Dict[str, Any] = None):
        self.verdict = verdict
        self.reason = reason
        self.metadata = metadata or {}

    def __repr__(self):
        return f"FilterResult(verdict={self.verdict}, reason={self.reason}, metadata={self.metadata})"
