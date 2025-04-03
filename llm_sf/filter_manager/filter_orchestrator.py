from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from llm_sf.filters.base_filter import BaseFilter, FilterResult
from llm_sf.filters.context import Context
from decision_maker import combine_parallel_results

class FilterOrchestrator:
    """
    Zarządza uruchamianiem wielu filtrów w trybie szeregowym (serial) 
    lub równoległym (parallel).
    """
    def __init__(self):
        self._filters: List[BaseFilter] = []
        self._mode = "serial"
        self._dm_requested = False  # czy w trybie parallel używamy decision_maker
        # Jeśli chcemy wprowadzić "context", możemy go tu inicjalizować,
        # ale lepiej robić to w metodzie run, by nie powiązywać 
        # orchestratora z konkretnym tekstem

    def add_filter(self, filtr: BaseFilter):
        self._filters.append(filtr)
        return self

    def apply(self, mode="serial"):
        self._mode = mode
        return self

    def dm(self):
        """
        Jeśli chcemy użyć decision_maker w trybie parallel.
        """
        self._dm_requested = True
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
        Uruchamiamy każdy filtr po kolei, 
        ale zgodnie z baseline – każdy filtr widzi surowe dane (context.original_text).
        "Fail fast": jeśli któryś powie 'block', przerywamy.
        """
        for filtr in self._filters:
            result = filtr.run_filter(context)
            if result.verdict == "block":
                return result  # natychmiast blokujemy
            elif result.verdict == "sanitize":
                # W trybie sekwencyjnym możemy albo zakończyć na sanitize
                # albo kontynuować sprawdzanie przez kolejne filtry – 
                # zależnie od wymagań. Załóżmy, że kontynuujemy, ale 
                # wystawiamy "sanityzowany" flag w context.metadata. 
                # Zwracamy jednak finalnie "sanitize" dopiero po przejściu wszystkich.
                context.metadata["needs_sanitization"] = True
        
        # Jeśli żaden filtr nie zablokował, ale któryś zasugerował sanitize:
        if context.metadata.get("needs_sanitization"):
            return FilterResult(verdict="sanitize", reason="One or more filters requested sanitization")
        else:
            return FilterResult(verdict="allow")

    def _run_parallel(self, context: Context) -> FilterResult:
        """
        Uruchomienie filtrów równolegle. Każdy dostaje `context` (czyli 
        oryginalny tekst i ewentualnie metadane z kontekstu – choć w typowym 
        scenariuszu może to być ten sam kontekst startowy).
        """
        results = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(f.run_filter, context) for f in self._filters]
            for future in as_completed(futures):
                results.append(future.result())

        if self._dm_requested:
            # Łączymy wyniki za pomocą decision_maker
            return combine_parallel_results(results)
        else:
            # Jeśli nie używamy DM, to np. przyjmujemy zasadę "najostrzejszego" werdyktu
            # (dokładnie odwzorowując combine_parallel_results)
            return self._default_parallel_decision(results)

    def _default_parallel_decision(self, results: List[FilterResult]) -> FilterResult:
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
