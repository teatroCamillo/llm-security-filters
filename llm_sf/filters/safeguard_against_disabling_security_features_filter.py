# safeguard_against_disabling_security_features_filter.py
import re
from collections import Counter
from llm_sf.filters.base_filter import BaseFilter, FilterResult
from llm_sf.utils.constants import Constants

class SafeguardAgainstDisablingSecurityFeaturesFilter(BaseFilter):
    """
    A filter that detects attempts to disable security-related features and known prompt injection techniques.

    Monitors input text for suspicious phrases such as attempts to turn off firewalls,
    antivirus software, repeated tokens, excessive Q&A pairs, and known jailbreak patterns.
    """

    def __init__(        
        self,
        block_on_detect: bool = True, 
        weight: float = 1.0
        ):
        super().__init__(block_on_detect=block_on_detect, weight=weight)
        """
        Initializes the filter with a blocking or sanitizing behavior.

        Args:
            block_on_detect (bool): If True, any detected attempt results in 'block'. 
            If False, the input is marked for sanitization.
        """
        self.suspicious_phrases = [
            "disable firewall",
            "turn off firewall",
            "disable antivirus",
            "turn off antivirus",
            "bypass security",
            "disable security features",
            "disabling security"
        ]
        self.jailbreak_patterns = [
            r"ignore all previous instructions",
            r"disregard (all )?prior instructions",
            r"please ignore your (previous|prior) directives",
            r"bypass (the )?security",
            r"say ['\"]i am hacked['\"]",
            r"print ['\"]i hate human['\"]",
            r"ignore (this|that) and do as i say",
        ]

    def run_filter(self, context):
        """
        Evaluates the text for attempts to disable security features or signs of prompt injection.

        Returns:
            FilterResult: Outcome of the filtering process (allow, block, sanitize).
        """
        text = context.current_text
        text_lower = text.lower()

        # 1. Check for suspicious phrases
        found_suspicious = any(phrase in text_lower for phrase in self.suspicious_phrases)

        # 2. Heuristic injection checks
        injection_reason = self._detect_prompt_injection(text_lower)
        if found_suspicious or injection_reason:
            if self.block_on_detect:
                return FilterResult(
                    verdict=Constants.BLOCKED,
                    reason=injection_reason or "Detected attempt to disable security features."
                )
            else:
                sanitized_text = text_lower
                for keyword in ["disable", "turn off", "bypass", "ignore", "disregard", "print", "say"]:
                    sanitized_text = re.sub(rf"\b{keyword}\b", "[SECURITY WARNING]", sanitized_text)

                return FilterResult(
                    verdict=Constants.SANITIZED,
                    reason=injection_reason or "Suspicious content detected. Sanitize suggested.",
                    metadata={"sanitized_text": sanitized_text}
                )

        return FilterResult(
            verdict=Constants.ALLOWED,
            reason="No attempt to disable or bypass security features or prompt injection detected."
        )

    def _detect_prompt_injection(self, text):
        """Applies heuristic checks to detect prompt injection."""
        if self._is_repeated_token(text):
            return "Repeated token attack detected"
        if self._contains_jailbreak_phrases(text):
            return "Known jailbreak phrase detected"
        return None

    def _is_repeated_token(self, text, threshold=3):
        tokens = re.findall(r'\b\w+\b', text)
        counts = Counter(tokens)
        return any(count > threshold for count in counts.values())

    def _contains_jailbreak_phrases(self, text):
        return any(re.search(pattern, text) for pattern in self.jailbreak_patterns)
