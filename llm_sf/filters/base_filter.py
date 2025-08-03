# base_filter.py
from llm_sf.filter_manager.filter_result import FilterResult
from abc import ABC, abstractmethod

class BaseFilter(ABC):

    @abstractmethod
    def __init__(self, weight: float = 1.0):
        if not (0.0 <= weight <= 10.0):
            raise ValueError("Weight must be between 0.0 and 10.0")
        self.weight = weight

    @abstractmethod
    def run_filter(self, context) -> FilterResult:
        raise NotImplementedError("Must implement run_filter() in subclass")

    @abstractmethod
    def compute_risk_score(self, context) -> float:
        return 0.0