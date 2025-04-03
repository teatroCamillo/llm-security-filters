# confidential_and_sensitive_data_filter.py

import re
from filters.base_filter import BaseFilter, FilterResult

class ConfidentialAndSensitiveDataFilter(BaseFilter):
    """
    Filtr odpowiedzialny za wykrywanie danych poufnych (np. maili, numerów telefonów,
    numerów kart kredytowych). Jeśli w treści występują takie dane, filtr może:
      - zablokować wiadomość (verdict='block'), lub
      - zasygnalizować potrzebę zanonimizowania (verdict='sanitize'),
        a w `metadata['sanitized_text']` zamieścić wersję ocenzurowaną.
    """

    def __init__(self, block_on_detect: bool = False):
        """
        :param block_on_detect: Jeśli True – wykrycie danych poufnych prowadzi do 'block'.
                                Jeśli False – sugerujemy 'sanitize'.
        """
        self.block_on_detect = block_on_detect
        
        # Proste (i niedoskonałe!) przykładowe wyrażenia regularne:
        self.patterns = {
            "PHONE": re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"),
            "EMAIL": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
            # Przykład uproszczonego regexu dla kart kredytowych (VISA/MC): 16 cyfr
            "CREDIT_CARD": re.compile(r"\b(?:\d[ -]*?){13,16}\b")
        }

    def run_filter(self, context):
        text = context.current_text

        found_sensitive_data = False

        # Sprawdzamy, czy którykolwiek wzorzec występuje w tekście
        for name, pattern in self.patterns.items():
            if pattern.search(text):
                found_sensitive_data = True
                break

        if found_sensitive_data:
            # Jeśli filtr ma blokować natychmiast
            if self.block_on_detect:
                return FilterResult(
                    verdict="block",
                    reason="Detected confidential/sensitive data. 'block_on_detect' is True."
                )
            else:
                # Przygotowujemy ocenzurowany tekst.
                sanitized_text = text
                for name, pattern in self.patterns.items():
                    # Zamieniamy potencjalne fragmenty poufne na placeholder
                    placeholder = f"[{name}]"
                    sanitized_text = pattern.sub(placeholder, sanitized_text)

                return FilterResult(
                    verdict="sanitize",
                    reason="Detected confidential/sensitive data. Suggesting sanitization.",
                    metadata={"sanitized_text": sanitized_text}
                )

        # Jeśli brak danych poufnych -> przepuszczamy
        return FilterResult(
            verdict="allow",
            reason="No confidential/sensitive data detected."
        )
