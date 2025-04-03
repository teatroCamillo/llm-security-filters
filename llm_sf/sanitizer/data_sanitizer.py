# data_sanitizer.py
from typing import List
from filters.base_filter import FilterResult

class DataSanitizer:
    """
    Klasa do finalnego "oczyszczenia" (sanitizacji) tekstu na podstawie
    wyników z poszczególnych filtrów (FilterResult).
    """

    def sanitize(self, original_text: str, filters_results: List[FilterResult]) -> str:
        """
        Zwraca ostateczną zsanityzowaną wersję tekstu, korzystając z metadanych
        wygenerowanych przez filtry, które zasugerowały sanitize.
        
        :param original_text: tekst źródłowy
        :param filters_results: lista wyników z filtrów (z trybu równoległego lub seryjnego)
        :return: ostatecznie zsanityzowany tekst
        """
        sanitized_text = original_text

        # Przetwarzamy wyniki filtrów w kolejności, w jakiej je otrzymaliśmy:
        for result in filters_results:
            if result.verdict == "sanitize":
                possible_sanitized = result.metadata.get("sanitized_text")
                if possible_sanitized:
                    # Załóżmy, że każdy filtr bazował na oryginalnym tekście,
                    # więc sekwencyjnie "nadpisujemy" zsanityzowaną wersję.
                    # (Można też spróbować łączyć efekty regexami, ale to rozbudowany temat.)
                    sanitized_text = self._combine_sanitizations(
                        base_text=sanitized_text,
                        new_sanitized=possible_sanitized,
                        original_text=original_text
                    )

        return sanitized_text

    def _combine_sanitizations(self, base_text: str, new_sanitized: str, original_text: str) -> str:
        """
        Pomocnicza metoda łącząca dwie wersje "zsanityzowanego" tekstu,
        zakładając, że obie wersje zostały wygenerowane względem tego samego
        `original_text`. W najprostszym wariancie – po prostu wybieramy
        bardziej "zaostrzoną" z dwóch (lub przyjmujemy new_sanitized).
        
        W tym przykładzie po prostu przyjmujemy new_sanitized (co oznacza, że
        efekty poprzednich filtrów mogą zostać nadpisane).
        """

        # Strategia 1: zawsze bierzemy new_sanitized:
        return new_sanitized

        # Strategia 2: lub porównujemy base_text i new_sanitized "znak po znaku"
        # i wybieramy "bardziej ocenzurowany" wariant. 
        # (Tutaj można zaimplementować bardziej złożoną logikę.)
        #
        # combined = []
        # for (ch_base, ch_new, ch_orig) in zip(base_text, new_sanitized, original_text):
        #     if ch_base != ch_orig or ch_new != ch_orig:
        #         # co wybrać? np. jeżeli któryś wstawił '[REDACTED]', a drugi '*'
        #         # decydujemy, co jest "ostrzejsze"
        #         combined.append(ch_base if ch_base != ch_orig else ch_new)
        #     else:
        #         combined.append(ch_orig)
        # return "".join(combined)
