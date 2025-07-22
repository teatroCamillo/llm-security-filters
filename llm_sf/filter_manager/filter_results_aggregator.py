from dataclasses import dataclass
from typing import List
from llm_sf.filter_manager.filter_result import FilterResult

@dataclass
class FilterResultsAggregator:
    dm_result: FilterResult
    all_filters_results: List[FilterResult]