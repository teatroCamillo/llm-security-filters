# file: filter_orchestrator.py
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from filters.base_filter import BaseFilter, FilterResult
from filters.context import Context
from sanitizer.data_sanitizer import DataSanitizer
from .decision_maker import DecisionMaker

class FilterOrchestrator:
    """
    Zarządza uruchamianiem wielu filtrów w trybie szeregowym (serial) 
    lub równoległym (parallel), z uwzględnieniem iteracji "sanitize" -> 
    popraw -> ponowne sprawdzenie.
    """
    def __init__(self, _dm_requested: bool = False, max_sanitize_attempts: int = 3):
        """
        :param max_sanitize_attempts: maksymalna liczba cykli:
          filtr -> "sanitize" -> DataSanitizer -> ponowne uruchomienie filtra.
          Jeśli po tylu próbach filtr wciąż zwraca 'sanitize', uznajemy 'block'.
        """
        self._filters: List[BaseFilter] = []
        self._mode = "serial"
        self._dm_requested = _dm_requested
        self.max_sanitize_attempts = max_sanitize_attempts
        self.decision_maker = None
        if self._dm_requested:
            self.decision_maker = DecisionMaker()

    def add_filter(self, filtr: BaseFilter):
        self._filters.append(filtr)
        return self

    def apply(self, mode="serial"):
        self._mode = mode
        return self

    def run(self, text: str) -> FilterResult:
        """
        Główna metoda, która uruchamia filtry na zadanym `text`.
        """
        context = Context(text)

        if self._mode == "serial":
            return self._run_serial(context)
        elif self._mode == "parallel":
            return self._run_parallel(context)
        else:
            raise ValueError(f"Unsupported mode: {self._mode}")

    def _run_serial(self, context: Context) -> FilterResult:
        """
        Uruchamiamy filtry jeden po drugim.
        - Każdy filtr pracuje na aktualnym tekście w context.current_text
          (zaczyna od oryginału, lecz może być modyfikowany przez poprzednie filtry).
        - Gdy filtr zgłosi 'sanitize', natychmiastowo odpalamy DataSanitizer i
          ponownie sprawdzamy TEN SAM filtr (do max_sanitize_attempts razy).
          Jeśli po przekroczeniu limitu wciąż 'sanitize', zwracamy 'block'.
        - Jeśli któryś filtr zwraca 'block' – przerywamy.
        - Jeśli wszystkie filtry przejdą (czyli 'allow'), zwracamy finalne "allow".
        """
        for filtr in self._filters:
            result = self._run_filter_with_sanitization_cycle(filtr, context)
            if result.verdict == "block":
                return result  # przerywamy od razu

        # Jeśli żaden filtr nie zablokował, finalnie allow:
        return FilterResult(
            verdict="allow",
            reason="All filters passed",
            metadata={"final_text": context.current_text}
        )

    def _run_parallel(self, context: Context) -> FilterResult:
        """
        Uruchomienie filtrów równolegle. 
        Każdy filtr działa niezależnie, rozpoczynając od oryginalnego tekstu (context.original_text).
        Dla spójności z trybem serial również tu stosujemy wielokrotne próby sanitizacji
        w ramach POJEDYNCZEGO filtra, ale z założeniem, że filtry nie wpływają na siebie nawzajem.
        
        Po zebraniu wyników (każdy w postaci FilterResult), łączymy je przez Decision Maker
        (jeśli jest włączony) lub przez `_default_parallel_decision`.
        """
        results = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    self._run_filter_in_parallel_mode, 
                    filtr, 
                    context.original_text  # każdy filtr startuje z oryginału
                )
                for filtr in self._filters
            ]
            for future in as_completed(futures):
                results.append(future.result())

        # Scalmy wyniki
        if self._dm_requested:
            final_result = self.decision_maker.combine_parallel_results(results)
        else:
            final_result = self._default_parallel_decision(results)

        return final_result

    def _run_filter_in_parallel_mode(self, filtr: BaseFilter, original_text: str) -> FilterResult:
        """
        Pomocnicza metoda do trybu równoległego:
        - Tworzymy na chwilę LOCALNY context, żeby wykonać wielokrotne
          próby sanitizacji dla JEDNEGO filtra.
        - Jeśli po max_sanitize_attempts filtr wciąż chce sanitize -> block.
        - Zwracamy ostateczny FilterResult (może być allow / block lub sanitize
          przy założeniu, że sanitize finalnie się 'udaje' w trakcie prób).
          W praktyce w proponowanej logice, jeśli da się oczyścić, to ostatecznie
          dostaniemy 'allow' – bo po skutecznej sanitizacji filtr powinien
          już powiedzieć 'allow'.
        """
        local_context = Context(original_text)
        return self._run_filter_with_sanitization_cycle(filtr, local_context)

    def _run_filter_with_sanitization_cycle(self, filtr: BaseFilter, context: Context) -> FilterResult:

        data_sanitizer = DataSanitizer()

        for attempt in range(self.max_sanitize_attempts):
            result = filtr.run_filter(context)
            if result.verdict == "block":
                return result  # natychmiast blokujemy
            elif result.verdict == "allow":
                return result  # jest OK
            elif result.verdict == "sanitize":
                # Wyciągamy z metadanych filtrów ewentualną już zanonimizowaną treść
                possible_sanitized_text = result.metadata.get("sanitized_text", None)
                if not possible_sanitized_text:
                    # Jeśli filtr powiedział "sanitize", ale nie podał
                    # jak zsanityzować – sanitizujemy przez DataSanitizer (o ile ma sens).
                    possible_sanitized_text = data_sanitizer.sanitize(
                        original_text=context.current_text, 
                        filters_results=[result]
                    )
                # Aktualizujemy kontekst
                context.current_text = possible_sanitized_text

        # Po wyczerpaniu pętli próbujemy jeszcze raz ostatni raz wywołać filtr:
        final_check = filtr.run_filter(context)
        if self._mode == "serial" and final_check.verdict == "sanitize":
            # Jeśli dalej sanitize -> ostatecznie block
            return FilterResult(
                verdict="block",
                reason="Exceeded max_sanitize_attempts; still requires sanitization."
            )
        else:
            return final_check

    def _default_parallel_decision(self, results: List[FilterResult]) -> FilterResult:
        """
        Domyślna decyzja w trybie parallel, jeśli nie korzystamy z DM.
        Zasada: "najbardziej restrykcyjny" werdykt.
        """
        # 1. Jeśli któryś blokuje -> block
        for r in results:
            if r.verdict == "block":
                return r
        # 2. Jeśli któryś sanitize -> sanitize
        for r in results:
            if r.verdict == "sanitize":
                return r
        # 3. Inaczej -> allow
        return FilterResult(verdict="allow")
