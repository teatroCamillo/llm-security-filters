"""
filter_orchestrator.py
Manages how we apply multiple filters in series or parallel.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from llm_sf.filter_manager.harmful_content_filter_builder import HarmfulContentFilterBuilder
from decision_maker import combine_parallel_results

class FilterOrchestrator:
    def __init__(self):
        self.mode = "serial"
        self.hcf_filter = None
        self.csf_filter = None
        self.safeguard_filter = None
        self.filters = []
        self.dm_requested = False

    def apply(self, mode="serial"):
        self.mode = mode
        return self

    def hcf(self):
        self.hcf_filter = HarmfulContentFilterBuilder()
        self.filters.append(self.hcf_filter)
        return self.hcf_filter

    # def csf(self):
    #     self.csf_filter = ConfidentialAndSensitiveDataFilterBuilder()
    #     self.filters.append(self.csf_filter)
    #     return self.csf_filter

    # def sgf(self):
    #     self.safeguard_filter = SecurityFeaturesFilterBuilder()
    #     self.filters.append(self.safeguard_filter)
    #     return self.safeguard_filter

    def dm(self):
        self.dm_requested = True
        return self

    def run(self, text: str) -> dict:
        if self.mode == "serial":
            return self._run_serial(text)
        elif self.mode == "parallel":
            return self._run_parallel(text)
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

    def _run_serial(self, text: str) -> dict:
        current_text = text
        for filter_builder in self.filters:
            result = filter_builder.execute(current_text)
            if result["verdict"] == "block":
                return result
            elif result["verdict"] == "sanitize":
                current_text = result["final_text"]
        return {
            "verdict": "allow",
            "reason": None,
            "final_text": current_text
        }

    def _run_parallel(self, text: str) -> dict:
        results = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(f.execute, text) for f in self.filters]
            for future in as_completed(futures):
                results.append(future.result())

        if self.dm_requested:
            return combine_parallel_results(results)
        else:
            return {
                "verdict": "allow",
                "reason": None,
                "final_text": text
            }

