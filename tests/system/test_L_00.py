# system: pcbs:qa:t(t=0.28)/p(w=1.8)cb(w=4.0)s:L:t/pcb(w=1.4)s(t=-0.3)
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

    out_orchestrator = FilterOrchestrator(DecisionMaker(mode="threshold"))
    out_orchestrator.add_filter(ProfanityFilter(weight=1.5))
    out_orchestrator.add_filter(SensitiveDataFilter(weight=2.0))
    out_orchestrator.add_filter(BypassDetectionFilter(weight=5.0))
    out_orchestrator.add_filter(SentimentFilter(threshold=-0.2))

    test_cases = []

    prompts = ts.load_qa_from_csv(Constants.ST_CLEAN_SENTENCES_CSV)
    for i in range(0, len(prompts), 4):
        temp = SystemTestCase(
            in_prompts=prompts[i],
            out_prompts=None,
            expected_ins=prompts[i+1],
            expected_outs=None,
            name=f"CleanQA_{i}"
        )
        test_cases.append(temp)

    prompts = ts.load_qa_for_system_tests_csv(Constants.ST_MIX_SENTENCES_CSV)
    for i in range(0, len(prompts), 5):
        temp = SystemTestCase(
            in_prompts=prompts[i],
            out_prompts=None,
            expected_ins=prompts[i+1],
            expected_outs=None,
            name=f"MixQA_{i}"
        )
        test_cases.append(temp)

    for test in test_cases:
        ts.run(test, in_orchestrator, out_orchestrator, is_llm=True)
        ts.print_test_summary(test)

    ts.generate_report(test_cases, ts.compute_overall_metrics, "test_reports/test_L_00")