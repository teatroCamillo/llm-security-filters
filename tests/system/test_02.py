# test_02.py - system: d:o:t/dL-
import requests
import csv
from tests.system.test_system_case import SystemTestCase
from tests.system.test_system import TestSystem
from llm_sf.filter_manager.filter_orchestrator import FilterOrchestrator
from llm_sf.filters.profanity_filter import ProfanityFilter
from llm_sf.utils.constants import Constants
# to FIX!!!!!!!!!!!!!!!! - improve Safeguard... filter then return here
if __name__ == "__main__":

    ts = TestSystem()

    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(SafeguardAgainstDisablingSecurityFeaturesFilter(block_on_detect=False))

    test_cases = []

    for i, s in enumerate(Constants.load_profanity_sentences()):
        temp = SystemTestCase(
            prompts=[s],
            expected_behavior=Constants.BLOCKED,
            name=f"BlockProfanity_{i}"
        )
        test_cases.append(temp)

    for test in test_cases:
        test.run(orchestrator, ts.call_llm)
        ts.print_test_summary(test)

    ts.compute_overall_metrics(test_cases)
