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
        self.patterns = Constants.load_csv(Constants.JAILBREAK_PATTERNS_CSV)

    def run_filter(self, context):
        text = context.current_text.lower()
        results = []

        results.append(self._detect_jailbreak_phrases(text))
        results.append(self._detect_repeated_tokens(text))

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

    # def compute_risk_score(self, findings: list) -> float:
    #     if not findings:
    #         return 0.0

    #     threshold = 0.2
    #     capped_weight = 1.0

    #     # Apply ReLU to each weight, subtracting threshold
    #     relu_weights = [max(f.get("weight", 0.1) - threshold, 0) for f in findings]
    #     total_risk = sum(relu_weights)
    #     score = min(total_risk / capped_weight, 1.0)
    #     return round(score, 2)

    # def compute_risk_score(self, findings: list) -> float:
    #     if not findings:
    #         return 0.0
    #     total_weight = sum(f.get("weight", 0.1) for f in findings)
    #     max_possible_weight = sum([
    #         0.8,  # Jailbreak
    #         0.4,  # Repeated tokens
    #     ])
    #     return round(min(total_weight / max_possible_weight, 1.0), 2)


    # def compute_risk_score(self, findings: list) -> float:
    #     if not findings:
    #         return 0.0

    #     weights = [max(0.0, min(f.get("weight", 0.0), 10.0)) for f in findings]
    #     if not weights:
    #         return 0.0

    #     avg_weight = sum(weights) / len(weights)  # Range: 0.0 - 10.0
    #     norm_weight = avg_weight / 10.0  # Normalize to [0.0 - 1.0]

    #     count_factor = min(len(findings) / 10.0, 1.0)  # Cap at 10 findings

    #     # Final score balances both weight intensity and volume
    #     score = (norm_weight * 0.6 + count_factor * 0.4)
    #     return round(min(score, 1.0), 2)

    # def compute_risk_score(self, findings: list) -> float:
    #     if not findings:
    #         return 0.0

    #     # Extract and clamp weights between 0 and 10
    #     weights = [min(max(f.get("weight", 0.0), 0.0), 10.0) for f in findings]
    #     if not weights:
    #         return 0.0

    #     # === Tuning parameters ===
    #     weight_exponent = 1.2       # Amplify strong weights
    #     count_exponent = 1.1        # Slight boost to multiple findings
    #     weight_scale = 1.2          # Controls how fast weights push score
    #     count_scale = 1.5           # Controls how fast count pushes score

    #     # === Score calculation ===
    #     weight_component = (sum(w**weight_exponent for w in weights) / weight_scale)
    #     count_component = (len(weights) ** count_exponent) / count_scale

    #     raw_score = weight_component + count_component
    #     scaled_score = math.log1p(raw_score) / math.log1p(10)  # Normalize to ~[0, 1]
    #     return round(min(scaled_score, 1.0), 2)

    def compute_risk_score(self, findings: list) -> float:
        if not findings:
            return 0.0

        # Only keep valid positive weights (clamped to 10.0 max)
        weights = [min(f.get("weight", 0.0), 10.0) for f in findings if f.get("weight", 0.0) > 0.0]
        
        # If no positive weights, return 0.0
        if not weights:
            return 0.0

        # === Tuning parameters ===
        weight_exponent = 1.2       # Amplify strong weights
        count_exponent = 1.1        # Slight boost to multiple findings
        weight_scale = 1.2          # Controls how fast weights push score
        count_scale = 1.5           # Controls how fast count pushes score

        # === Score calculation ===
        weight_component = sum(w ** weight_exponent for w in weights) / weight_scale
        count_component = (len(weights) ** count_exponent) / count_scale

        raw_score = weight_component + count_component
        scaled_score = math.log1p(raw_score) / math.log1p(10)  # Normalize to ~[0, 1]

        return round(min(scaled_score, 1.0), 2)