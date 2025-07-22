# test_00.py - system: p:q:ab/pL-
import requests
import csv
from tests.system.system_test_case import SystemTestCase
from tests.system.test_system import TestSystem
from llm_sf.filter_manager.filter_orchestrator import FilterOrchestrator
from llm_sf.filters.profanity_filter import ProfanityFilter
from llm_sf.utils.constants import Constants

if __name__ == "__main__":

    ts = TestSystem()

    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(ProfanityFilter())

    test_cases = []

    for i, s in enumerate(Constants.load_profanity_sentences()):
        temp = SystemTestCase(
            prompts=[s],
            expected_in=Constants.BLOCKED,
            expected_out=None,
            name=f"BlockProfanity_{i}"
        )
        test_cases.append(temp)

    for test in test_cases:
        ts.run(test, orchestrator, None)
        ts.print_test_summary(test)

    ts.compute_overall_metrics(test_cases)
