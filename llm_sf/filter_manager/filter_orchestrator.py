# filter_orchestrator.py
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from llm_sf.filters.base_filter import BaseFilter
from llm_sf.filter_manager.context import Context
from llm_sf.filter_manager.filter_result import FilterResult
from llm_sf.filter_manager.filter_results_aggregator import FilterResultsAggregator
from llm_sf.filter_manager.decision_maker import DecisionMaker

class FilterOrchestrator:

    def __init__(self, dm: DecisionMaker = DecisionMaker()):
        self._filters: List[BaseFilter] = []
        self.decision_maker = dm

    def add_filter(self, filtr: BaseFilter):
        self._filters.append(filtr)
        return self

    def run(self, text: str) -> FilterResultsAggregator:
        context = Context(text)
        results = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    self._run_filter,
                    filtr,
                    context
                )
                for filtr in self._filters
            ]
            for future in as_completed(futures):
                results.append(future.result())

        return FilterResultsAggregator(self.decision_maker.make_decision(results), results)

    def _run_filter(self, filtr: BaseFilter, context: Context) -> FilterResult:
        return filtr.run_filter(context)
