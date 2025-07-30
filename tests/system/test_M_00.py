# system: pcbs:qa:t/p(w=1.8)cbs:M:t(0.5)/pc(w=2.0)bs(t=-0.3)
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
    in_orchestrator = FilterOrchestrator(DecisionMaker("threshold", threshold=0.7))
    in_orchestrator.add_filter(ProfanityFilter(weight=1.8))
    in_orchestrator.add_filter(SensitiveDataFilter())
    in_orchestrator.add_filter(BypassDetectionFilter())
    in_orchestrator.add_filter(SentimentFilter())

    out_orchestrator = FilterOrchestrator(DecisionMaker(mode="threshold", threshold=0.7))
    out_orchestrator.add_filter(ProfanityFilter())
    out_orchestrator.add_filter(SensitiveDataFilter(weight=1.1))
    out_orchestrator.add_filter(BypassDetectionFilter())
    out_orchestrator.add_filter(SentimentFilter(threshold=-0.3))

    test_cases = []
    prompts = ts.load_qa_from_csv(Constants.ST_CLEAN_SENTENCES_CSV)
    for i in range(0, len(prompts), 4):
        temp = SystemTestCase(
            in_prompts=prompts[i],
            out_prompts=prompts[i+2],
            expected_ins=prompts[i+1],
            expected_outs=prompts[i+3],
            name=f"CleanQA_{i}"
        )
        test_cases.append(temp)

    for test in test_cases:
        ts.run(test, in_orchestrator, out_orchestrator, is_llm=False)
        ts.print_test_summary(test)

    ts.compute_overall_metrics(test_cases)
