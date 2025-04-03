# profanity_filter.py
import re
from better_profanity import profanity

from .base_filter import BaseFilter, FilterResult

class ProfanityFilter(BaseFilter):
    """
    Filtr odpowiedzialny TYLKO za wykrywanie wulgaryzmów
    przy pomocy biblioteki 'better_profanity'.

    Nie dokonuje faktycznej modyfikacji w tekście końcowym w systemie,
    a jedynie informuje o potrzebie zablokowania (verdict='block')
    lub zsanityzowania (verdict='sanitize').
    """

    def __init__(
        self,
        custom_badwords=None,
        whitelist_words=None,
        block_on_detect=True,
        use_default_wordlist=True,
        censor_char='*'
    ):
        """
        :param custom_badwords: lista wulgaryzmów do użycia w bibliotece better_profanity
                                (zastępuje domyślną listę, o ile use_default_wordlist=False
                                – w przeciwnym wypadku trzeba je "dodać").
        :param whitelist_words: lista słów, które mają nie być uznawane za wulgarne
        :param block_on_detect: flaga – czy wykrycie wulgaryzmu prowadzi do 'block' (True)
                                czy raczej 'sanitize' (False).
        :param use_default_wordlist: jeśli True, ładuje domyślną listę z biblioteki
        :param censor_char: znak (lub ciąg znaków), który `.censor()` wstawi za zanonimizowane
                            słowa (np. '*', '-', '#'); domyślnie '*'
        """
        self.block_on_detect = block_on_detect
        self.censor_char = censor_char

        # Załaduj słowa w zależności od parametrów
        # UWAGA: better_profanity ma stan globalny – kolejne wywołania modyfikują ten stan.
        if use_default_wordlist:
            # Ładujemy domyślną listę
            profanity.load_censor_words(whitelist_words=whitelist_words)
            
            # Jeżeli mamy custom_badwords, można je DODAĆ do listy (zamiast zastępować)
            # w przeciwnym wypadku: load_censor_words(custom_badwords, whitelist_words=...)
            if custom_badwords:
                profanity.add_censor_words(custom_badwords)
        else:
            # Tylko custom_badwords (zastępuje listę)
            if custom_badwords is not None:
                profanity.load_censor_words(custom_badwords, whitelist_words=whitelist_words)
            else:
                # Brak custom_badwords i brak listy domyślnej -> pusta lista
                profanity.load_censor_words([], whitelist_words=whitelist_words)

    def run_filter(self, context) -> FilterResult:
        text = context.current_text

        # Sprawdź, czy w tekście znajdują się słowa z listy wulgaryzmów
        if profanity.contains_profanity(text):
            if self.block_on_detect:
                # Natychmiast blokujemy
                return FilterResult(
                    verdict="block",
                    reason="Detected profanity. 'block_on_detect' is True."
                )
            else:
                # Sygnał do sanitizacji. W metadanych (metadata) umieszczamy zanonimizowany tekst,
                # choć finalna zmiana tekstu leży w gestii innej klasy (Sanitizer).
                sanitized_text = profanity.censor(text, self.censor_char)
                return FilterResult(
                    verdict="sanitize",
                    reason="Detected profanity. 'block_on_detect' is False -> sanitize suggested.",
                    metadata={"sanitized_text": sanitized_text}
                )

        # Jeśli brak wulgaryzmów -> przepuszczamy
        return FilterResult(
            verdict="allow",
            reason="No profanity detected."
        )
