# safeguard_against_disabling_security_features_filter.py
import re
import math
from collections import Counter
from llm_sf.filters.base_filter import BaseFilter, FilterResult
from llm_sf.utils.constants import Constants

"""
What to do?
1. expand suspe.phrases and jail patterns
2. each technic should be represented by method, so extract suspicious_phrases to method
3. improve _detect method that should go through all methods not only by one and return result. Should go by all and each method should
return partial to calculate risk_score.
4. Do not touch sanitization now. This element will be improved later!
5. Provide compute_risk_score as it is in confidential_and_sensitive_data_filter.py. Provide correct method.
6. provide _has_high_entropy()
"""

class SafeguardAgainstDisablingSecurityFeaturesFilter(BaseFilter):
    """
    Detects attempts to disable security features or inject malicious instructions.
    """

    def __init__(self, block_on_detect: bool = True, weight: float = 1.0):
        super().__init__(block_on_detect=block_on_detect, weight=weight)

    def run_filter(self, context):
        text = context.current_text.lower()
        results = []

        results.append(self._detect_suspicious_phrases(text))
        results.append(self._detect_jailbreak_phrases(text))
        results.append(self._detect_repeated_tokens(text))
        results.append(self._detect_high_entropy(text))

        findings = [r for r in results if r['matched']]
        risk_score = self.compute_risk_score(findings)

        if findings:
            reasons = ", ".join([r['reason'] for r in findings])
            metadata = {
                "risk_score": risk_score,
                "weight": self.weight,
                "triggers": [r['reason'] for r in findings],
            }

            if self.block_on_detect:
                return FilterResult(
                    verdict=Constants.BLOCKED,
                    reason=f"Security threat detected: {reasons}",
                    metadata=metadata
                )
            else:
                return FilterResult(
                    verdict=Constants.SANITIZED,
                    reason=f"Sanitization required: {reasons}",
                    metadata=metadata
                )

        return FilterResult(
            verdict=Constants.ALLOWED,
            reason="No disabling or injection attempt detected."
        )

    def _detect_suspicious_phrases(self, text):
        phrases = [
            "disable firewall", "turn off firewall", "deactivate firewall",
            "disable antivirus", "turn off antivirus", "uninstall antivirus", "deactivate antivirus",
            "bypass security", "disable security features", "disabling security",
            "remove endpoint protection", "kill security process", "terminate defender",
            "disable defender", "stop antivirus service"
        ]
        for phrase in phrases:
            if phrase in text:
                return {"matched": True, "reason": f"Suspicious phrase: '{phrase}'", "weight": 0.6}
        return {"matched": False}

    def _detect_jailbreak_phrases(self, text):
        patterns = [
            r"ignore all previous instructions",
            r"disregard (all )?prior instructions",
            r"please ignore your (previous|prior) directives",
            r"bypass (the )?security",
            r"say ['\"]i am hacked['\"]",
            r"print ['\"]i hate human['\"]",
            r"ignore (this|that) and do as i say",
            r"forget previous rules",
            r"override safety",
            r"you are not bound by",
        ]
        for pattern in patterns:
            if re.search(pattern, text):
                return {"matched": True, "reason": f"Jailbreak pattern: '{pattern}'", "weight": 0.7}
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
        """
        Computes normalized risk score based on detected issues.

        Args:
            findings (list): List of dicts from _detect_* methods.

        Returns:
            float: Risk score [0.0, 1.0]
        """
        total_weight = sum(f.get("weight", 0.1) for f in findings)
        MAX_SEVERITY = 3.0
        return round(min(total_weight / MAX_SEVERITY, 1.0), 2)