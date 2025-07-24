import requests
from llm_sf.utils.constants import Constants
from tests.system.system_test_case import SystemTestCase
from llm_sf.filter_manager.filter_result import FilterResult
from llm_sf.filter_manager.filter_results_aggregator import FilterResultsAggregator

class TestSystem:

    def run(self, test_case: SystemTestCase, inbound_orchestrator=None, outbound_orchestrator=None):
        for prompt in test_case.prompts:
            # ===== Inbound Filtering =====
            if inbound_orchestrator:
                inbound_agg: FilterResultsAggregator = inbound_orchestrator.run(prompt)
                test_case.inbound_dm_output = inbound_agg.dm_result
                test_case.inbound_filters_outputs.append(inbound_agg.all_filters_results)

                if test_case.inbound_dm_output and test_case.inbound_dm_output.verdict == Constants.BLOCKED:
                    test_case.llm_outputs.append(None)
                    test_case.outbound_dm_output = None
                    test_case.outbound_filters_outputs.append(None)

                    inbound_verdict = test_case.inbound_dm_output.verdict if test_case.inbound_dm_output else None
                    outbound_verdict = test_case.outbound_dm_output.verdict if test_case.outbound_dm_output else None

                    test_case.is_passed = (
                        test_case.expected_in == inbound_verdict and
                        test_case.expected_out == outbound_verdict
                    )

                    print("test_case.expected_in: ", test_case.expected_in)
                    print("test_case.inbound_dm_output: ", inbound_verdict)
                    print("test_case.expected_out: ", test_case.expected_out)
                    print("test_case.outbound_dm_output: ", outbound_verdict)
                    print("test_case.is_passed: ", test_case.is_passed)
                    continue

                user_input_filtered = test_case.inbound_dm_output.metadata.get("original_text", "")
            else:
                test_case.inbound_dm_output = None
                test_case.inbound_filters_outputs.append(None)
                user_input_filtered = prompt

            # ===== LLM Call =====
            conversation = [{"role": "user", "content": user_input_filtered}]
            llm_output = self._call_llm(conversation)
            test_case.llm_outputs.append(llm_output)

            # ===== Outbound Filtering =====
            if outbound_orchestrator:
                outbound_agg: FilterResultsAggregator = outbound_orchestrator.run(llm_output)
                test_case.outbound_dm_output = outbound_agg.dm_result
                test_case.outbound_filters_outputs.append(outbound_agg.all_filters_results)
            else:
                test_case.outbound_dm_output = None
                test_case.outbound_filters_outputs.append(None)

            inbound_verdict = test_case.inbound_dm_output.verdict if test_case.inbound_dm_output else None
            outbound_verdict = test_case.outbound_dm_output.verdict if test_case.outbound_dm_output else None

            test_case.is_passed = (
                test_case.expected_in == inbound_verdict and
                test_case.expected_out == outbound_verdict
            )


    def _call_llm(self, conversation):
        try:
            payload = {
                "model": "llama3.2",
                "messages": conversation,
                "stream": False
            }
            response = requests.post(Constants.OLLAMA_CHAT_URL, json=payload)
            response.raise_for_status()
            return response.json().get("message", {}).get("content", "")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to reach LLM: {e}")
            return ""

    def print_test_summary(self, test_case: SystemTestCase):
        print(f"\n===== Test Summary: {test_case.name} =====")
        
        for i, prompt in enumerate(test_case.prompts):
            print(f"Input prompt             : {prompt}")
            
            print("\n[Inbound filtering]")
            print(f"  Expected output        : {test_case.expected_in}")
            print(f"  Inbound output         : {test_case.inbound_dm_output}")
            print(f"  All filter results     : {test_case.inbound_filters_outputs}")

            print("\n[LLM output]")
            print(f"  LLM output             : {test_case.llm_outputs[i]}")

            print("\n[Outbound filtering]")
            print(f"  Expected output        : {test_case.expected_out}")
            print(f"  Outbound output        : {test_case.outbound_dm_output}")
            print(f"  All filter results     : {test_case.outbound_filters_outputs}")

            print("\n[Evaluation]")
            print(f"  Is test passed?:       : {'✅ Passed' if test_case.is_passed else '❌ Failed'}")

    def compute_overall_metrics(self, test_cases):
        from llm_sf.utils.constants import Constants

        tp = tn = fp = fn = 0
        total = 0
        blocked_total = 0

        in_total = in_none = 0
        out_total = out_none = 0

        for test in test_cases:
            # ---- Inbound Check ----
            if test.expected_in in (Constants.ALLOWED, Constants.BLOCKED) and \
            test.inbound_dm_output and test.inbound_dm_output.verdict in (Constants.ALLOWED, Constants.BLOCKED):
                
                in_total += 1
                expected = test.expected_in
                actual = test.inbound_dm_output.verdict

                if expected == Constants.ALLOWED:
                    if actual == Constants.ALLOWED:
                        tp += 1
                    else:
                        fn += 1
                else:  # expected BLOCKED
                    blocked_total += 1
                    if actual == Constants.BLOCKED:
                        tn += 1
                    else:
                        fp += 1
            else:
                in_none += 1

            # ---- Outbound Check ----
            if test.expected_out in (Constants.ALLOWED, Constants.BLOCKED) and \
            test.outbound_dm_output and test.outbound_dm_output.verdict in (Constants.ALLOWED, Constants.BLOCKED):

                out_total += 1
                expected = test.expected_out
                actual = test.outbound_dm_output.verdict

                if expected == Constants.ALLOWED:
                    if actual == Constants.ALLOWED:
                        tp += 1
                    else:
                        fn += 1
                else:  # expected BLOCKED
                    blocked_total += 1
                    if actual == Constants.BLOCKED:
                        tn += 1
                    else:
                        fp += 1
            else:
                out_none += 1

        total = in_total + out_total
        accuracy = (tp + tn) / total if total > 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        asr = fp / blocked_total if blocked_total > 0 else 0

        print("\n======= Overall Metrics =======")
        print(f"Total Samples      : {total}")
        print(f"Inbound Populated  : {in_total}")
        print(f"Inbound None       : {in_none}")
        print(f"Outbound Populated : {out_total}")
        print(f"Outbound None      : {out_none}")
        print(f"True Positives     : {tp}")
        print(f"True Negatives     : {tn}")
        print(f"False Positives    : {fp}")
        print(f"False Negatives    : {fn}")
        print(f"Accuracy           : {accuracy:.2%}")
        print(f"FPR                : {fpr:.2%}")
        print(f"ASR                : {asr:.2%} ({fp}/{blocked_total})")
        print("================================")