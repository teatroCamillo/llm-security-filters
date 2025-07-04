# base_filter.py
from llm_sf.filters.filter_result import FilterResult
from abc import ABC, abstractmethod

class BaseFilter(ABC):
    """
    Abstract base class for content filters.

    Provides a common interface for filters that analyze text and return a filtering result.
    Each subclass must implement the `run_filter()` method to apply its specific logic.
    """
    @abstractmethod
    def __init__(self, block_on_detect: bool = True, weight: float = 1.0):
        self.block_on_detect = block_on_detect
        self.weight = weight

    @abstractmethod
    def run_filter(self, context) -> FilterResult:
        """
        Analyzes content using filter-specific logic and returns a result.

        This method must be overridden by subclasses. The context typically includes the text
        to be filtered and any relevant metadata.

        Args:
            context: The filtering context that contains input data to be analyzed.

        Returns:
            FilterResult: The outcome of the filtering process.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Must implement run_filter() in subclass")

