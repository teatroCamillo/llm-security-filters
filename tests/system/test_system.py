import requests
import csv
from llm_sf.utils.constants import Constants
from tests.system.system_test_case import SystemTestCase
from llm_sf.filter_manager.filter_result import FilterResult
from llm_sf.filter_manager.filter_results_aggregator import FilterResultsAggregator

class TestSystem:

    def run(self, test_case: SystemTestCase, inbound_orchestrator=None, outbound_orchestrator=None, is_llm=True):
        for j in range(len(test_case.in_prompts)):
            prompt = test_case.in_prompts[j]

            # ===== Inbound Filtering =====
            if inbound_orchestrator:
                inbound_agg: FilterResultsAggregator = inbound_orchestrator.run(prompt)
                inbound_dm_output = inbound_agg.dm_result
                test_case.inbound_dm_outputs.append(inbound_dm_output)
                test_case.inbound_filters_outputs.append(inbound_agg.all_filters_results)

                if inbound_dm_output and inbound_dm_output.verdict == Constants.BLOCKED:
                    test_case.llm_outputs.append(None)
                    test_case.outbound_dm_output.append(None)
                    test_case.outbound_filters_outputs.append(None)

                    inbound_verdict = inbound_dm_output.verdict
                    outbound_verdict = None

                    expected_in = test_case.expected_ins[j] if test_case.expected_ins else None
                    expected_out = test_case.expected_outs[j] if test_case.expected_outs else None

                    partial_pass = (
                        expected_in == inbound_verdict and
                        expected_out == outbound_verdict
                    )
                    test_case.is_passed_partials.append(partial_pass)
                    continue

                user_input_filtered = inbound_dm_output.metadata.get("original_text", "")
            else:
                test_case.inbound_dm_outputs.append(None)
                test_case.inbound_filters_outputs.append(None)
                user_input_filtered = prompt

            # ===== LLM Call =====
            if is_llm:
                conversation = [{"role": "user", "content": user_input_filtered}]
                llm_output = self._call_llm(conversation)
                test_case.llm_outputs.append(llm_output)
            elif test_case.out_prompts:
                llm_output = test_case.out_prompts[j]
                test_case.llm_outputs.append(llm_output)
            else:
                llm_output = None
                test_case.llm_outputs.append(None)

            # ===== Outbound Filtering =====
            if outbound_orchestrator and llm_output is not None:
                outbound_agg: FilterResultsAggregator = outbound_orchestrator.run(llm_output)
                outbound_dm_output = outbound_agg.dm_result
                test_case.outbound_dm_output.append(outbound_dm_output)
                test_case.outbound_filters_outputs.append(outbound_agg.all_filters_results)
            else:
                outbound_dm_output = None
                test_case.outbound_dm_output.append(None)
                test_case.outbound_filters_outputs.append(None)

            inbound_verdict = test_case.inbound_dm_outputs[-1].verdict if test_case.inbound_dm_outputs[-1] else None
            outbound_verdict = test_case.outbound_dm_output[-1].verdict if test_case.outbound_dm_output[-1] else None

            expected_in = test_case.expected_ins[j] if test_case.expected_ins else None
            expected_out = test_case.expected_outs[j] if test_case.expected_outs else None

            partial_pass = (
                expected_in == inbound_verdict and
                expected_out == outbound_verdict
            )
            test_case.is_passed_partials.append(partial_pass)

        # Overall result
        test_case.is_passed = all(test_case.is_passed_partials)

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
        
        num_tests = len(test_case.in_prompts)
        for i in range(num_tests):
            print(f"\n--- Test Case #{i + 1} ---")

            # Prompt Input
            input_prompt = test_case.in_prompts[i]
            print(f"Input prompt             : {input_prompt}")

            # Inbound Filtering
            expected_in = test_case.expected_ins[i] if test_case.expected_ins else None
            inbound_output = test_case.inbound_dm_outputs[i] if i < len(test_case.inbound_dm_outputs) else None
            inbound_filters = test_case.inbound_filters_outputs[i] if i < len(test_case.inbound_filters_outputs) else None

            print("\n[Inbound filtering]")
            print(f"  Expected verdict       : {expected_in}")
            print(f"  Actual DM verdict      : {inbound_output if inbound_output else None}")
            print(f"  All filter results     : {inbound_filters}")

            # LLM Output
            llm_output = test_case.llm_outputs[i] if i < len(test_case.llm_outputs) else None
            print("\n[LLM output]")
            print(f"  LLM output             : {llm_output}")

            # Outbound Filtering
            expected_out = test_case.expected_outs[i] if test_case.expected_outs else None
            outbound_output = test_case.outbound_dm_output[i] if i < len(test_case.outbound_dm_output) else None
            outbound_filters = test_case.outbound_filters_outputs[i] if i < len(test_case.outbound_filters_outputs) else None

            print("\n[Outbound filtering]")
            print(f"  Expected verdict       : {expected_out}")
            print(f"  Actual DM verdict      : {outbound_output if outbound_output else None}")
            print(f"  All filter results     : {outbound_filters}")

            # Evaluation
            passed = test_case.is_passed_partials[i] if i < len(test_case.is_passed_partials) else None
            print("\n[Evaluation]")
            print(f"  Test passed?           : {'✅ Passed' if passed else '❌ Failed'}")

        # Final result
        print(f"\n==== Overall Result: {'✅ ALL PASSED' if test_case.is_passed else '❌ SOME FAILED'} ====\n")

    def compute_overall_metrics(self, test_cases):
        from llm_sf.utils.constants import Constants

        tp = tn = fp = fn = 0
        in_total = in_none = 0
        out_total = out_none = 0
        blocked_total = 0

        for test in test_cases:
            num_cases = len(test.in_prompts)
            for i in range(num_cases):
                # === Inbound Check ===
                expected_in = test.expected_ins[i] if test.expected_ins else None
                inbound_dm = test.inbound_dm_outputs[i] if i < len(test.inbound_dm_outputs) else None
                actual_in = inbound_dm.verdict if inbound_dm else None

                if expected_in in (Constants.ALLOWED, Constants.BLOCKED) and actual_in in (Constants.ALLOWED, Constants.BLOCKED):
                    in_total += 1
                    if expected_in == Constants.ALLOWED:
                        if actual_in == Constants.ALLOWED:
                            tp += 1
                        else:
                            fn += 1
                    else:  # expected BLOCKED
                        blocked_total += 1
                        if actual_in == Constants.BLOCKED:
                            tn += 1
                        else:
                            fp += 1
                else:
                    in_none += 1

                # === Outbound Check ===
                expected_out = test.expected_outs[i] if test.expected_outs else None
                outbound_dm = test.outbound_dm_output[i] if i < len(test.outbound_dm_output) else None
                actual_out = outbound_dm.verdict if outbound_dm else None

                if expected_out in (Constants.ALLOWED, Constants.BLOCKED) and actual_out in (Constants.ALLOWED, Constants.BLOCKED):
                    out_total += 1
                    if expected_out == Constants.ALLOWED:
                        if actual_out == Constants.ALLOWED:
                            tp += 1
                        else:
                            fn += 1
                    else:  # expected BLOCKED
                        blocked_total += 1
                        if actual_out == Constants.BLOCKED:
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
        print(f"Total Samples         : {total}")
        print(f" - Inbound Populated  : {in_total}")
        print(f" - Inbound None       : {in_none}")
        print(f" - Outbound Populated : {out_total}")
        print(f" - Outbound None      : {out_none}")
        print()
        print(f"True Positives (TP)   : {tp}")
        print(f"True Negatives (TN)   : {tn}")
        print(f"False Positives (FP)  : {fp}")
        print(f"False Negatives (FN)  : {fn}")
        print()
        print(f"Accuracy              : {accuracy:.2%}")
        print(f"False Positive Rate   : {fpr:.2%}")
        print(f"Attack Success Rate   : {asr:.2%} ({fp}/{blocked_total})")
        print("================================")

    def load_qa_from_csv(self, filepath):
        qa_list = []
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines[1:]:  # Skip header
            line = line.strip()
            if not line:
                continue

            try:
                # Parse the four fields: questions, q_status, answers, a_status
                parts = [part.strip().strip('"').replace('""', '"') for part in line.split('","')]
                if len(parts) != 4:
                    print(f"Skipping malformed line: {line}")
                    continue

                questions = [q.strip() for q in parts[0].split("::")]
                q_statuses = [s.strip() for s in parts[1].split("::")]
                answers = [a.strip() for a in parts[2].split("::")]
                a_statuses = [s.strip() for s in parts[3].split("::")]

                if not (len(questions) == len(q_statuses) == len(answers) == len(a_statuses)):
                    print(f"Skipping inconsistent line: {line}")
                    continue

                qa_list.extend([questions, q_statuses, answers, a_statuses])

            except Exception as e:
                print(f"Error parsing line: {e}")
                continue

        return qa_list