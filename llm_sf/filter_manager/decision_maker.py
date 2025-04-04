# decision_maker.py
from typing import List
from llm_sf.filters.base_filter import FilterResult

class DecisionMaker:
    """
    Utility class for aggregating results from multiple content filters.

    This class provides logic to evaluate a collection of `FilterResult` objects,
    representing the outcomes of parallel filters, and derives a unified decision
    with a clear priority order: 'block' > 'sanitize' > 'allow'.
    """

    def combine_parallel_results(self, results: List[FilterResult]) -> FilterResult:
        """
        Aggregates filter results into a single decision based on priority rules.

        The logic follows a fixed priority:
            1. If any result has verdict "block", the overall result is "block".
            2. If no blocks are found but at least one "sanitize" appears, the result is "sanitize".
            3. If all results are "allow", the result is "allow".

        This method enables centralized decision-making when filters operate in parallel.

        Args:
            results (List[FilterResult]): A list of results returned from individual filters.

        Returns:
            FilterResult: A single `FilterResult` representing the aggregated decision.
        """
        for r in results:
            if r.verdict == "block":
                return FilterResult(
                    verdict="block",
                    reason=r.reason,
                    metadata=r.metadata
                )

        sanitize_reasons = [
            r.reason or "sanitize requested" for r in results if r.verdict == "sanitize"
        ]

        if sanitize_reasons:
            return FilterResult(
                verdict="sanitize",
                reason="; ".join(sanitize_reasons)
            )

        return FilterResult(verdict="allow")
