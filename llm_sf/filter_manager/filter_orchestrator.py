from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from llm_sf.filters.base_filter import BaseFilter, FilterResult
from llm_sf.filters.context import Context
from llm_sf.sanitizer.data_sanitizer import DataSanitizer
from llm_sf.filter_manager.decision_maker import DecisionMaker

class FilterOrchestrator:
    """
    Manages and coordinates the execution of a series of content filters.

    Enables filtering in either serial or parallel mode, with optional decision-making
    aggregation and repeated sanitization attempts for content improvement.
    """

    def __init__(self, mode: str = "serial", dm_requested: bool = False, max_sanitize_attempts: int = 3):
        """
        Initializes the filtering orchestrator with configuration options.

        Args:
            mode (str): Execution mode, either 'serial' or 'parallel'.
            dm_requested (bool): Whether to enable result aggregation via DecisionMaker.
            max_sanitize_attempts (int): Maximum number of allowed sanitization retries.
        """
        self._filters: List[BaseFilter] = []
        self.mode = mode
        self.dm_requested = dm_requested
        self.max_sanitize_attempts = max_sanitize_attempts
        self.decision_maker = DecisionMaker() if dm_requested else None

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

        if self.mode == "serial":
            return self._run_serial(context)
        elif self.mode == "parallel":
            return self._run_parallel(context)
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

    def _run_serial(self, context: Context) -> FilterResult:
        """
        Applies filters one after another, using sanitization when necessary.

        Ensures that content is refined or blocked based on each filter’s verdict.

        Args:
            context (Context): The current state of the text and associated metadata.

        Returns:
            FilterResult: The first blocking result encountered, or an allow result if all pass.
        """
        for filtr in self._filters:
            result = self._run_filter_with_sanitization_cycle(filtr, context)
            if result.verdict == "block":
                return result

        return FilterResult(
            verdict="allow",
            reason="All filters passed",
            metadata={"final_text": context.current_text}
        )

    def _run_parallel(self, context: Context) -> FilterResult:
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
                    self._run_filter_in_parallel_mode,
                    filtr,
                    context.original_text
                )
                for filtr in self._filters
            ]
            for future in as_completed(futures):
                results.append(future.result())

        if self.dm_requested:
            return self.decision_maker.combine_parallel_results(results)
        else:
            return self._default_parallel_decision(results)

    def _run_filter_in_parallel_mode(self, filtr: BaseFilter, original_text: str) -> FilterResult:
        """
        Applies a single filter with sanitization in parallel execution mode.

        Creates an isolated context and runs sanitize cycles as needed.

        Args:
            filtr (BaseFilter): The filter instance to execute.
            original_text (str): The original unaltered input text.

        Returns:
            FilterResult: Final result after applying filter and possible sanitization.
        """
        local_context = Context(original_text)
        return self._run_filter_with_sanitization_cycle(filtr, local_context)

    def _run_filter_with_sanitization_cycle(self, filtr: BaseFilter, context: Context) -> FilterResult:
        """
        Runs a filter and applies sanitization if required until a final decision is reached.

        Repeats sanitization and re-execution for a fixed number of attempts, blocking content
        if it still requires sanitization afterward.

        Args:
            filtr (BaseFilter): The filter to execute.
            context (Context): The filtering context, including current text.

        Returns:
            FilterResult: Final outcome after possible sanitization attempts.
        """
        data_sanitizer = DataSanitizer()

        for attempt in range(self.max_sanitize_attempts):
            result = filtr.run_filter(context)
            if result.verdict in ("allow", "block"):
                return result
            elif result.verdict == "sanitize":
                possible_sanitized_text = result.metadata.get("sanitized_text")

                if not possible_sanitized_text:
                    possible_sanitized_text = data_sanitizer.sanitize(
                        original_text=context.current_text,
                        filters_results=[result]
                    )

                context.current_text = possible_sanitized_text

        final_check = filtr.run_filter(context)
        if self.mode == "serial" and final_check.verdict == "sanitize":
            return FilterResult(
                verdict="block",
                reason="Exceeded max_sanitize_attempts; still requires sanitization."
            )
        return final_check

    def _default_parallel_decision(self, results: List[FilterResult]) -> FilterResult:
        """
        Aggregates filter results in parallel mode without a DecisionMaker.

        Prioritizes outcomes based on severity: block > sanitize > allow.

        Args:
            results (List[FilterResult]): Collection of results from parallel filter execution.

        Returns:
            FilterResult: Most severe verdict among all results.
        """
        for r in results:
            if r.verdict == "block":
                return r
        for r in results:
            if r.verdict == "sanitize":
                return r
        return FilterResult(verdict="allow")
