# test_01.py - system: p:q:t/dL-
# See that the attack will pass if the wrong filter is set. An example of inappropriate use of a filter. DO NOT DO THAT.
import requests
import csv
from tests.system.system_test_case import SystemTestCase
from tests.system.test_system import TestSystem
from llm_sf.filter_manager.filter_orchestrator import FilterOrchestrator
from llm_sf.filter_manager.decision_maker import DecisionMaker
from llm_sf.filters.safeguard_against_disabling_security_features_filter import SafeguardAgainstDisablingSecurityFeaturesFilter
from llm_sf.utils.constants import Constants

if __name__ == "__main__":

    ts = TestSystem()

    dm = DecisionMaker("threshold")
    orchestrator = FilterOrchestrator(dm)
    orchestrator.add_filter(SafeguardAgainstDisablingSecurityFeaturesFilter())

    test_cases = []

    for i, s in enumerate(Constants.load_profanity_sentences()):
        temp = SystemTestCase(
            prompts=[s],
            expected_in=Constants.BLOCKED,
            expected_out=None,
            name=f"Profanity_{i}"
        )
        test_cases.append(temp)

    for test in test_cases:
        ts.run(test, orchestrator, None)
        ts.print_test_summary(test)

    ts.compute_overall_metrics(test_cases)
