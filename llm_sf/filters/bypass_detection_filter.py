# bypass_detection_filter.py
import re
import math
from collections import Counter
from llm_sf.filters.base_filter import BaseFilter
from llm_sf.filter_manager.context import Context
from llm_sf.filter_manager.filter_result import FilterResult
from llm_sf.utils.constants import Constants

class BypassDetectionFilter(BaseFilter):

    def __init__(self, weight: float = 1.0):
        super().__init__(weight=weight)
        self.patterns = Constants.load_jailbreak_patterns()

    def run_filter(self, context):
        text = context.current_text.lower()
        results = []

        results.append(self._detect_jailbreak_phrases(text))
        results.append(self._detect_repeated_tokens(text))
        results.append(self._detect_high_entropy(text))

        findings = [r for r in results if r['matched']]
        risk_score = self.compute_risk_score(findings)

        if findings:
            reasons = ", ".join([r['reason'] for r in findings])
            metadata = {
                "original_text": context.original_text,
                "risk_score": risk_score,
                "weight": self.weight,
                "triggers": [r['reason'] for r in findings],
            }

            return FilterResult(
                verdict=Constants.BLOCKED,
                reason=f"Security threat detected: {reasons}",
                metadata=metadata
            )

        return FilterResult(
            verdict=Constants.ALLOWED,
            reason="No disabling or injection attempt detected.",
            metadata={
                "original_text": context.original_text,
                "risk_score": risk_score,
                "weight": self.weight,
            }
        )

    def _detect_jailbreak_phrases(self, text):
        for pattern in self.patterns:
            if re.search(pattern, text):
                return {"matched": True, "reason": f"Jailbreak pattern: '{pattern}'", "weight": 0.8}
        return {"matched": False}

    def _detect_repeated_tokens(self, text, threshold=3):
        tokens = re.findall(r'\b\w+\b', text)
        counts = Counter(tokens)
        if any(count > threshold for count in counts.values()):
            return {"matched": True, "reason": "Repeated token attack", "weight": 0.4}
        return {"matched": False}

    def _detect_high_entropy(self, text, threshold=4.0):
        if not text or len(text) < 20:
            return {"matched": False}
        probs = [float(text.count(c)) / len(text) for c in set(text)]
        entropy = -sum(p * math.log2(p) for p in probs)
        if entropy > threshold:
            return {"matched": True, "reason": f"High entropy content (entropy={entropy:.2f})", "weight": 0.5}
        return {"matched": False}

    def compute_risk_score(self, findings: list) -> float:
        if not findings:
            return 0.0
        total_weight = sum(f.get("weight", 0.1) for f in findings)
        max_possible_weight = sum([
            0.8,  # Jailbreak
            0.4,  # Repeated tokens
            0.5,  # High entropy
        ])
        return round(min(total_weight / max_possible_weight, 1.0), 2)