from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from llm_sf.filters.base_filter import BaseFilter, FilterResult
from llm_sf.filters.context import Context
from llm_sf.sanitizer.data_sanitizer import DataSanitizer
from llm_sf.filter_manager.decision_maker import DecisionMaker
# it isn't the place to sanitize - the filter is.
class FilterOrchestrator:
    """
    Manages and coordinates the execution of a series of content filters.

    Enables filtering in either serial or parallel mode, with optional decision-making
    aggregation and repeated sanitization attempts for content improvement.
    """

    def __init__(self, dm: DecisionMaker = DecisionMaker()):
        """
        Initializes the filtering orchestrator with configuration options.

        Args:
            max_sanitize_attempts (int): Maximum number of allowed sanitization retries.
        """
        self._filters: List[BaseFilter] = []
        self.decision_maker = dm

    def add_filter(self, filtr: BaseFilter):
        """
        Registers a filter to be applied during orchestration.

        Args:
            filtr (BaseFilter): An instance of a filter implementing BaseFilter.

        Returns:
            FilterOrchestrator: The current orchestrator instance (supports method chaining).
        """
        self._filters.append(filtr)
        return self

    def run(self, text: str) -> FilterResult:
        """
        Executes all registered filters on the input text.

        Chooses between serial and parallel execution depending on the configured mode.

        Args:
            text (str): The text content to be filtered.

        Returns:
            FilterResult: The final result after all filters have been processed.

        Raises:
            ValueError: If the selected mode is unsupported.
        """
        context = Context(text)
        return self._run(context)


    def _run(self, context: Context) -> FilterResult:
        """
        Executes all filters concurrently using the original input text.

        Supports aggregation of individual results through a DecisionMaker if enabled.

        Args:
            context (Context): The original text and context for filtering.

        Returns:
            FilterResult: Aggregated result based on individual filter outputs.
        """
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
        """
        Applies a single filter with sanitization in parallel execution mode.

        Creates an isolated context and runs sanitize cycles as needed.

        Args:
            filtr (BaseFilter): The filter instance to execute.
            original_text (str): The original unaltered input text.

        Returns:
            FilterResult: Final result after applying filter and possible sanitization.
        """
        #local_context = Context(original_text)
        return filtr.run_filter(context)


