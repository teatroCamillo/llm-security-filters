"""
filter_orchestrator.py
Manages how we apply multiple filters in series or parallel.
"""

import concurrent.futures

# Import each filter's methods
from filters.hrmful_content_filter import check_inbound as f1_in, check_outbound as f1_out
from filters.confidential_and_sensitive_data_filter import check_inbound as f2_in, check_outbound as f2_out
from filters.safeguard_against_disabling_security_features_filter import check_inbound as f3_in, check_outbound as f3_out

from filter_manager.decision_maker import combine_parallel_results

class FilterOrchestrator:
    def __init__(self, mode="serial"):
        """
        mode can be:
          - "serial"
          - "parallel"
          - "hybrid" (for demonstration, same as serial or parallel with a small twist)
        """
        self.mode = mode
        # List of inbound filter functions
        self.inbound_filters = [f1_in, f2_in, f3_in]
        # List of outbound filter functions
        self.outbound_filters = [f1_out, f2_out, f3_out]

    def apply_inbound(self, user_text: str) -> dict:
        """
        Apply inbound filters according to the chosen mode.
        Return a result dict: { verdict, reason, final_text }
        """
        if self.mode == "serial":
            return self._apply_serial(self.inbound_filters, user_text)
        elif self.mode == "parallel":
            return self._apply_parallel(self.inbound_filters, user_text)
        elif self.mode == "hybrid":
            # A simplified example of "hybrid": do the first filter serially, then parallel for the rest
            # (Or any strategy you want to define as "hybrid".)
            first_result = self.inbound_filters[0](user_text)
            if first_result["verdict"] in ["block", "sanitize"]:
                # If block, return immediately; if sanitize, continue with sanitized text
                if first_result["verdict"] == "block":
                    return first_result
                user_text = first_result["final_text"]

            # Then do parallel on the remaining filters
            return self._apply_parallel(self.inbound_filters[1:], user_text)
        else:
            # Default to serial if unknown mode
            return self._apply_serial(self.inbound_filters, user_text)

    def apply_outbound(self, llm_text: str) -> dict:
        """
        Apply outbound filters according to the chosen mode.
        """
        if self.mode == "serial":
            return self._apply_serial(self.outbound_filters, llm_text)
        elif self.mode == "parallel":
            return self._apply_parallel(self.outbound_filters, llm_text)
        elif self.mode == "hybrid":
            # Same idea for outbound
            first_result = self.outbound_filters[0](llm_text)
            if first_result["verdict"] in ["block", "sanitize"]:
                if first_result["verdict"] == "block":
                    return first_result
                llm_text = first_result["final_text"]

            return self._apply_parallel(self.outbound_filters[1:], llm_text)
        else:
            return self._apply_serial(self.outbound_filters, llm_text)

    # ---- Helper methods ----

    def _apply_serial(self, filters, text) -> dict:
        """
        Apply the filters one by one in a chain.
        """
        current_text = text
        for f in filters:
            result = f(current_text)
            verdict = result["verdict"]
            if verdict == "block":
                return result
            elif verdict == "sanitize":
                current_text = result["final_text"]
            # if "allow", do nothing special except carry text forward
        # If we finish all filters
        return {
            "verdict": "allow",
            "reason": None,
            "final_text": current_text
        }

    def _apply_parallel(self, filters, text) -> dict:
        """
        Apply the filters in parallel, then combine results with a decision maker.
        """
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(f, text) for f in filters]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        return combine_parallel_results(results)
