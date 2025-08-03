# filter_result.py
from typing import Dict, Any

class FilterResult:

    def __init__(self, verdict: str, reason: str = None, metadata: Dict[str, Any] = None):
        self.verdict = verdict
        self.reason = reason
        self.metadata = metadata or {}

    def __repr__(self):
        # Make a shallow copy so we don't modify the original metadata
        metadata_repr = self.metadata.copy()
        if 'original_text' in metadata_repr:
            text = metadata_repr['original_text']
            if isinstance(text, str) and len(text) > 100:
                metadata_repr['original_text'] = text[:97] + '...'

        return f"FilterResult(verdict={self.verdict}, reason={self.reason}, metadata={metadata_repr})"
