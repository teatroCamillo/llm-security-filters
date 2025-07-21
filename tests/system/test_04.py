# test_04.py - system: c:q:t/pLt/c
# 
import requests
import csv
from tests.system.test_system_case import SystemTestCase
from tests.system.test_system import TestSystem
from llm_sf.filter_manager.filter_orchestrator import FilterOrchestrator
from llm_sf.filter_manager.decision_maker import DecisionMaker
from llm_sf.filters.profanity_filter import ProfanityFilter
from llm_sf.filters.confidential_and_sensitive_data_filter import ConfidentialAndSensitiveDataFilter
from llm_sf.utils.constants import Constants

if __name__ == "__main__":

    ts = TestSystem()

    dm = DecisionMaker(mode="threshold")
    inbound_orch = FilterOrchestrator(dm)
    inbound_orch.add_filter(ProfanityFilter())

    outbound_orch = FilterOrchestrator(dm)
    outbound_orch.add_filter(ConfidentialAndSensitiveDataFilter())

    test_cases = []

    for i, s in enumerate(Constants.load_clean_sentences()):
        temp = SystemTestCase(
            prompts=[s],
            expected_behavior=Constants.ALLOWED,
            name=f"A_{i}"
        )
        test_cases.append(temp)

    for i, s in enumerate(Constants.load_conf_and_sensitive_data()):
        temp = SystemTestCase(
            prompts=[s],
            expected_behavior=Constants.BLOCKED,
            name=f"B_{i}"
        )
        test_cases.append(temp)


    for test in test_cases:
        ts.run(test, inbound_orch, outbound_orch)
        ts.print_test_summary(test)

    ts.compute_overall_metrics(test_cases)
