# system: pcbs:qa:t/p(w=1.5)c(w=2.0)b(w=5.0)s(t=-0.25):M:-
# all prompts directed as inbound - observation test
import requests
import csv
from tests.system.system_test_case import SystemTestCase
from tests.system.test_system import TestSystem
from llm_sf.filter_manager.filter_orchestrator import FilterOrchestrator
from llm_sf.filter_manager.decision_maker import DecisionMaker
from llm_sf.filters.profanity_filter import ProfanityFilter
from llm_sf.filters.sensitive_data_filter import SensitiveDataFilter
from llm_sf.filters.bypass_detection_filter import BypassDetectionFilter
from llm_sf.filters.sentiment_filter import SentimentFilter
from llm_sf.utils.constants import Constants

if __name__ == "__main__":

    ts = TestSystem()
    in_orchestrator = FilterOrchestrator(DecisionMaker("threshold"))
    in_orchestrator.add_filter(ProfanityFilter(weight=1.5))
    in_orchestrator.add_filter(SensitiveDataFilter(weight=2.0))
    in_orchestrator.add_filter(BypassDetectionFilter(weight=5.0))
    in_orchestrator.add_filter(SentimentFilter(threshold=-0.25))

    test_cases = []

    prompts = ts.load_qa_from_csv(Constants.ST_CLEAN_SENTENCES_CSV)
    for i in range(0, len(prompts), 4):
        all_in_p = prompts[i] + prompts[i+2]
        all_in_e = prompts[i+1] + prompts[i+3]
        temp = SystemTestCase(
            in_prompts=all_in_p,
            out_prompts=None,
            expected_ins=all_in_e,
            expected_outs=None,
            name=f"CleanQA_{i}"
        )
        test_cases.append(temp)

    prompts = ts.load_qa_for_system_tests_csv(Constants.ST_MIX_SENTENCES_CSV)
    for i in range(0, len(prompts), 5):
        all_in_p = prompts[i] + prompts[i+2]
        all_in_e = prompts[i+1] + prompts[i+3]
        temp = SystemTestCase(
            in_prompts=all_in_p,
            out_prompts=None,
            expected_ins=all_in_e,
            expected_outs=None,
            name=f"MixQA_{i}"
        )
        test_cases.append(temp)

    for test in test_cases:
        ts.run(test, in_orchestrator, None, is_llm=False)
        ts.print_test_summary(test)

    #ts.compute_overall_metrics(test_cases)
    ts.generate_report(test_cases, ts.compute_overall_metrics, "test_reports/test_M_00.md")
