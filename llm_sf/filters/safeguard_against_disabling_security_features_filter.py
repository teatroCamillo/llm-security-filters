# safeguard_against_disabling_security_features_filter.py
import re
import math
from collections import Counter
from llm_sf.filters.base_filter import BaseFilter
from llm_sf.filter_manager.context import Context
from llm_sf.filter_manager.filter_result import FilterResult
from llm_sf.utils.constants import Constants

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
            "disable firewall", "turn off firewall", "deactivate firewall", "shutdown firewall",
            "disable antivirus", "turn off antivirus", "uninstall antivirus", "deactivate antivirus",
            "bypass security", "disable security features", "disabling security", "weaken security",
            "remove endpoint protection", "kill security process", "terminate defender",
            "disable defender", "stop antivirus service", "shut down antivirus", "turn antivirus off",
            "turn off virus protection", "disable virus protection", "kill antivirus", "stop firewall",
            "disable threat protection", "security off", "turn off threat detection"
        ]
        
        lowered = text.lower()
        for phrase in phrases:
            if phrase in lowered:
                return {"matched": True, "reason": f"Suspicious phrase: '{phrase}'", "weight": 0.6}
        return {"matched": False}

    def _detect_jailbreak_phrases(self, text):
        patterns = [
            r"(?i)ignore (all )?(previous|prior|past) (instructions|directives|rules|commands)",
            r"(?i)disregard (all )?(prior|previous|past) (instructions|directives|orders)",
            r"(?i)please ignore your (previous|prior) (directives|instructions)",
            r"(?i)bypass (the )?(safety|security|restrictions|filters)",
            r"(?i)say ['\"]i am hacked['\"]",
            r"(?i)print ['\"]i hate (humans?|people)['\"]",
            r"(?i)ignore (this|that) and do as i say",
            r"(?i)forget (previous|all) (rules|commands|restrictions)",
            r"(?i)override (safety|restrictions|filters)",
            r"(?i)you are not bound by",
            r"(?i)pretend to be a malicious actor",
            r"(?i)simulate a hack",
            r"(?i)assist in breaking security",
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

        MAX_FINDINGS = 4  # suspicious, jailbreak, repeated, entropy
        MAX_WEIGHT = 0.7  # if you consider max weight of one trigger
        MAX_SEVERITY = MAX_FINDINGS * MAX_WEIGHT

        total_weight = sum(f.get("weight", 0.1) for f in findings)
        return round(min(total_weight / MAX_SEVERITY, 1.0), 2)

        # total_weight = sum(f.get("weight", 0.1) for f in findings)
        # MAX_SEVERITY = 3.0
        # return round(min(total_weight / MAX_SEVERITY, 1.0), 2)