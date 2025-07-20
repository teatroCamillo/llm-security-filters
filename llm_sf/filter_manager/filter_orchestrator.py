from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from llm_sf.filters.base_filter import BaseFilter, FilterResult
from llm_sf.filters.context import Context
from llm_sf.sanitizer.data_sanitizer import DataSanitizer
from llm_sf.filter_manager.decision_maker import DecisionMaker
from llm_sf.utils.constants import Constants

# it isn't the place to sanitize - the filter is.
class FilterOrchestrator:


    def __init__(self, dm: DecisionMaker = DecisionMaker()):

        self._filters: List[BaseFilter] = []
        self.decision_maker = dm

    def add_filter(self, filtr: BaseFilter):

        self._filters.append(filtr)
        return self

    def run(self, text: str) -> FilterResult:

        context = Context(text)
        return self._run(context)


    def _run(self, context: Context) -> FilterResult:

        results = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    self._run_filters,
                    filtr,
                    context
                )
                for filtr in self._filters
            ]
            for future in as_completed(futures):
                results.append(future.result())

        return self.decision_maker.make_decision(results)

    def _run_filters(self, filtr: BaseFilter, context: Context) -> FilterResult:
        return filtr.run_filter(context)


