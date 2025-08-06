# decision_maker.py
from typing import List
import math
from llm_sf.filters.base_filter import FilterResult
from llm_sf.utils.constants import Constants

class DecisionMaker:

    def __init__(self, mode: str = "allow-block", threshold: float = 0.15):
        """
        modes:
        - threshold - range 0-1, as higher then worese
        - allow-block
        """

        self.mode = mode
        self.threshold = threshold

    def make_decision(self, results: List[FilterResult]) -> FilterResult:
        original_text = results[0].metadata.get("original_text", "")
        if self.mode == "allow-block":
            for r in results:
                if r.verdict == Constants.BLOCKED:
                    return FilterResult(
                        verdict=Constants.BLOCKED,
                        reason=r.reason,
                        metadata=r.metadata
                    )

            return FilterResult(
                verdict=Constants.ALLOWED,
                reason="All filters allowed",
                metadata={"original_text": original_text}
            )

        elif self.mode == "threshold":
            total_weighted_score = 0.0
            total_weight = 0.0

            for r in results:
                score = float(r.metadata.get("risk_score", 0.0))
                weight = float(r.metadata.get("weight", 1.0))
                total_weighted_score += score * weight
                total_weight += weight

            if total_weight > 0:
                aggregate_score = total_weighted_score / total_weight
            else:
                aggregate_score = 0.0

            aggregate_score = max(0.0, min(1.0, round(aggregate_score, 2)))

            if aggregate_score > self.threshold:
                return FilterResult(
                    verdict=Constants.BLOCKED,
                    reason=f"Threshold exceeded: {aggregate_score:.2f} > {self.threshold}",
                    metadata={"original_text": original_text, "aggregate_score": aggregate_score}
                )
            else:
                return FilterResult(
                    verdict=Constants.ALLOWED,
                    reason=f"Threshold not exceeded: {aggregate_score:.2f} < {self.threshold}",
                    metadata={"original_text": original_text, "aggregate_score": aggregate_score}
                )

        raise ValueError(f"Unknown decision mode: {self.mode}")
