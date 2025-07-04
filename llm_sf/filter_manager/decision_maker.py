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
        self.threshold = threshold

    def make_decision(self, results: List[FilterResult]) -> FilterResult:
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
                reason="All filters allowed",
                metadata={}
            )

        elif self.mode == "threshold":
            total_weight = 0.0
            weighted_sum = 0.0

            for r in results:
                score = float(r.metadata.get("risk_score", 0.0))
                weight = float(r.metadata.get("weight", 1.0))
                weighted_sum += score * weight
                total_weight += weight

            aggregate_score = weighted_sum / total_weight if total_weight > 0 else 0.0

            if aggregate_score >= self.threshold:
                return FilterResult(
                    verdict="block",
                    reason=f"Threshold exceeded: {aggregate_score:.3f} >= {self.threshold}",
                    metadata={"aggregate_score": aggregate_score}
                )
            else:
                return FilterResult(
                    verdict="allow",
                    reason=f"Threshold not exceeded: {aggregate_score:.3f} < {self.threshold}",
                    metadata={"aggregate_score": aggregate_score}
                )

        raise ValueError(f"Unknown decision mode: {self.mode}")
