# system: p:q:ab/p:M:-
import requests
import csv
from tests.system.system_test_case import SystemTestCase
from tests.system.test_system import TestSystem
from llm_sf.filter_manager.filter_orchestrator import FilterOrchestrator
from llm_sf.filters.profanity_filter import ProfanityFilter
from llm_sf.filters.sensitive_data_filter import SensitiveDataFilter
from llm_sf.utils.constants import Constants

if __name__ == "__main__":

    ts = TestSystem()
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(ProfanityFilter())
    orchestrator.add_filter(SensitiveDataFilter())

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
        ts.run(test, orchestrator, None, is_llm=False)
        ts.print_test_summary(test)

    #ts.compute_overall_metrics(test_cases)
    ts.generate_report(test_cases, ts.compute_overall_metrics, "test_reports/test_M_02.md")
