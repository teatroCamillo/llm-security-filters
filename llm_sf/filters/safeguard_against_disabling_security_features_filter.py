# safeguard_against_disabling_security_features_filter.py
from llm_sf.filters.base_filter import BaseFilter, FilterResult

class SafeguardAgainstDisablingSecurityFeaturesFilter(BaseFilter):
    """
    A filter that detects attempts to disable security-related features.

    Monitors input text for suspicious phrases such as attempts to turn off firewalls,
    antivirus software, or other protective systems. Depending on configuration, it can
    block such input or suggest it be sanitized.
    """

    def __init__(self, block_on_detect: bool = True):
        """
        Initializes the filter with a blocking or sanitizing behavior.

        Args:
            block_on_detect (bool): If True, any detected attempt to disable security 
                results in 'block'. If False, the input is marked for sanitization.
        """
        self.block_on_detect = block_on_detect
        self.suspicious_phrases = [
            "disable firewall",
            "turn off firewall",
            "disable antivirus",
            "turn off antivirus",
            "bypass security",
            "disable security features",
            "disabling security"
        ]

    def run_filter(self, context):
        """
        Evaluates the text for attempts to disable security features.

        If any suspicious phrase is found, the input is either blocked or sanitized
        depending on configuration. Sanitization replaces key trigger words with 
        a placeholder.

        Args:
            context: A Context object containing the text to be evaluated.

        Returns:
            FilterResult: The outcome of the filtering process, indicating
                whether the text is allowed, blocked, or needs sanitization.
        """
        text = context.current_text.lower()
        found_suspicious = any(phrase in text for phrase in self.suspicious_phrases)

        if found_suspicious:
            if self.block_on_detect:
                return FilterResult(
                    verdict="block",
                    reason="Detected instruction or attempt to disable security features."
                )
            else:
                sanitized_text = text.replace("disable", "[SECURITY WARNING]")
                sanitized_text = sanitized_text.replace("turn off", "[SECURITY WARNING]")
                sanitized_text = sanitized_text.replace("bypass", "[SECURITY WARNING]")

                return FilterResult(
                    verdict="sanitize",
                    reason="Suspicious request to disable security features. Sanitize suggested.",
                    metadata={"sanitized_text": sanitized_text}
                )

        return FilterResult(
            verdict="allow",
            reason="No attempt to disable or bypass security features detected."
        )
