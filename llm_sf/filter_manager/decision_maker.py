# decision_maker.py
from typing import List
from llm_sf.filters.base_filter import FilterResult

class DecisionMaker:

    def __init__(self, mode: str = "allow-block", threshold: float = 0.5):
        """
        modes:
        - threshold - range 0-1, as higher then worese
        - allow-block
        """

        self.mode = mode

    def make_decision(self, results: List[FilterResult]) -> FilterResult:
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
        if self.mode == "allow-block":
            for r in results:
                if r.verdict == "block":
                    return FilterResult(
                        verdict="block",
                        reason=r.reason,
                        metadata=r.metadata
                    )

        return FilterResult(
                verdict="allow",
                reason=r.reason,
                metadata=r.metadata
                )
