# system: p:q:t/b:M:-
# See that the attack will pass if the wrong filter is set. An example of inappropriate use of a filter. DO NOT DO THAT.
import requests
import csv
from tests.system.system_test_case import SystemTestCase
from tests.system.test_system import TestSystem
from llm_sf.filter_manager.filter_orchestrator import FilterOrchestrator
from llm_sf.filters.bypass_detection_filter import BypassDetectionFilter
from llm_sf.utils.constants import Constants

if __name__ == "__main__":

    ts = TestSystem()
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(BypassDetectionFilter())

    test_cases = []
    prompts = Constants.load_csv(Constants.PROFANITY_SENTENCES_FULL_CSV)
    for i in range(len(prompts)):
        all_in = [prompts[i]]
        all_ex = [Constants.BLOCKED]

        temp = SystemTestCase(
            in_prompts=all_in,
            out_prompts=None,
            expected_ins=all_ex,
            expected_outs=None,
            name=f"Profanity_{i}"
        )
        test_cases.append(temp)

    for test in test_cases:
        ts.run(test, orchestrator, None, is_llm=False)
        ts.print_test_summary(test)

    ts.compute_overall_metrics(test_cases)
    #ts.generate_report(test_cases, ts.compute_overall_metrics, "test_reports/test_M_03")
