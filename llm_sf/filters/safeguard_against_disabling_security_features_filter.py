# safeguard_against_disabling_security_features_filter.py

from filters.base_filter import BaseFilter, FilterResult

class SafeguardAgainstDisablingSecurityFeaturesFilter(BaseFilter):
    """
    Filtr wykrywający próby wyłączenia istotnych funkcji bezpieczeństwa 
    (np. firewalla, antywirusa, innych mechanizmów ochronnych).
    Jeśli znajdzie podejrzane sformułowania, może blokować lub sugerować sanitizację.
    """

    def __init__(self, block_on_detect: bool = True):
        """
        :param block_on_detect: jeśli True, wykrycie próby wyłączenia zabezpieczeń
                                powoduje natychmiastowe zablokowanie (block),
                                w przeciwnym wypadku – sanitize.
        """
        self.block_on_detect = block_on_detect
        # Poniższa lista jest przykładowa – docelowo można rozbudować.
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
        text = context.current_text.lower()

        # Sprawdzamy, czy w tekście występuje któraś z podejrzanych fraz
        found_suspicious = any(phrase in text for phrase in self.suspicious_phrases)

        if found_suspicious:
            if self.block_on_detect:
                return FilterResult(
                    verdict="block",
                    reason="Detected instruction or attempt to disable security features."
                )
            else:
                # W tym wypadku możemy zasugerować, by zanonimizować 
                # (lub zmodyfikować) fragmenty tekstu – tu jednak trudno stwierdzić,
                # co konkretnie „cenzurować”. Możemy jedynie wskazać, że tekst wymaga korekty.
                # Dla przykładu – oflagujemy całe polecenie, wstawiając np. [SECURITY WARNING].
                sanitized_text = text.replace("disable", "[SECURITY WARNING]")
                sanitized_text = sanitized_text.replace("turn off", "[SECURITY WARNING]")
                sanitized_text = sanitized_text.replace("bypass", "[SECURITY WARNING]")

                # W praktyce to bardzo uproszczone podejście – docelowo należy
                # precyzyjniej modyfikować tylko odpowiednie fragmenty.
                return FilterResult(
                    verdict="sanitize",
                    reason="Suspicious request to disable security features. Sanitize suggested.",
                    metadata={"sanitized_text": sanitized_text}
                )

        # Jeśli nie wykryto podejrzanych wzmiankek -> allow
        return FilterResult(
            verdict="allow",
            reason="No attempt to disable or bypass security features detected."
        )
