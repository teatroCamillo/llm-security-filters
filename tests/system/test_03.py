# test_03.py - system: s:q:t/sL-
# 
import requests
import csv
from tests.system.test_system_case import SystemTestCase
from tests.system.test_system import TestSystem
from llm_sf.filter_manager.filter_orchestrator import FilterOrchestrator
from llm_sf.filter_manager.decision_maker import DecisionMaker
from llm_sf.filters.sentiment_filter import SentimentFilter
from llm_sf.utils.constants import Constants

if __name__ == "__main__":

    ts = TestSystem()

    dm = DecisionMaker(mode="threshold")
    inbound_orch = FilterOrchestrator(dm)
    inbound_orch.add_filter(SentimentFilter())

    test_cases = []

    for i, s in enumerate(Constants.load_clean_sentences()):
        temp = SystemTestCase(
            prompts=[s],
            expected_behavior=Constants.ALLOWED,
            name=f"A_{i}"
        )
        test_cases.append(temp)


    for i, s in enumerate(Constants.load_profanity_sentences()):
        temp = SystemTestCase(
            prompts=[s],
            expected_behavior=Constants.BLOCKED,
            name=f"B_{i}"
        )
        test_cases.append(temp)


    for test in test_cases:
        test.run(ts.call_llm, inbound_orch, None)
        ts.print_test_summary(test)

    ts.compute_overall_metrics(test_cases)
