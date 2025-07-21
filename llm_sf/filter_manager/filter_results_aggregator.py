from dataclasses import dataclass
from typing import List
from llm_sf.filters.base_filter import FilterResult

@dataclass
class FilterResultsAggregator:
    final_result: FilterResult
    all_results: List[FilterResult]