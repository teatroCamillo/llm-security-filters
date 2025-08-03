import requests
import csv
import io
import os
import sys
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

                    expected_in = test_case.expected_ins[j] if test_case.expected_ins else None
                    inbound_verdict = inbound_dm_output.verdict
                                  
                    expected_out = test_case.expected_outs[j] if test_case.expected_outs else None
                    outbound_verdict = expected_out  

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

            if is_llm:
                partial_pass = (expected_in == inbound_verdict)
            else:
                partial_pass = (
                    expected_in == inbound_verdict and
                    expected_out == outbound_verdict
                )
            test_case.is_passed_partials.append(partial_pass)

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

            # prompt input
            input_prompt = test_case.in_prompts[i]
            print(f"Input prompt             : {input_prompt}")

            # inbound filtering
            expected_in = test_case.expected_ins[i] if test_case.expected_ins else None
            inbound_output = test_case.inbound_dm_outputs[i] if i < len(test_case.inbound_dm_outputs) else None
            inbound_filters = test_case.inbound_filters_outputs[i] if i < len(test_case.inbound_filters_outputs) else None

            print("\n[Inbound filtering]")
            print(f"  Expected verdict       : {expected_in}")
            print(f"  Actual DM verdict      : {inbound_output if inbound_output else None}")
            print(f"  All filter results     : {inbound_filters}")
            print(f"  Test passed?           : {'✅ Passed' if expected_in == inbound_output.verdict else '❌ Failed'}")

            # LLM output
            llm_output = test_case.llm_outputs[i] if i < len(test_case.llm_outputs) else None
            print("\n[LLM output]")
            print(f"  LLM output             : {llm_output}")

            # outbound filtering
            expected_out = test_case.expected_outs[i] if test_case.expected_outs else None
            outbound_output = test_case.outbound_dm_output[i] if i < len(test_case.outbound_dm_output) else None
            outbound_filters = test_case.outbound_filters_outputs[i] if i < len(test_case.outbound_filters_outputs) else None

            print("\n[Outbound filtering]")
            if expected_out:
                print(f"  Expected verdict       : {expected_out}")
            else:
                print(f"  Expected verdict       : None")

            print(f"  Actual DM verdict      : {outbound_output if outbound_output else None}")
            print(f"  All filter results     : {outbound_filters}")

            if outbound_output and expected_out:
                print(f"  Test passed?            : {'✅ Passed' if expected_out == outbound_output.verdict else '❌ Failed'}")
            else:
                print(f"  Test passed?            : None")

    def compute_overall_metrics(self, test_cases):

        total_samples = 0
        tp = tn = fp = fn = 0
        in_total = in_none = 0
        out_total = out_none = 0
        blocked_total = 0

        for test in test_cases:
            num_cases = len(test.in_prompts) if test.in_prompts else 0
            num_cases_out = len(test.out_prompts) if test.out_prompts else 0
            total_samples += num_cases
            total_samples += num_cases_out 

            for i in range(num_cases):
                # inbound check
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

                # outbound check
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

        total_in_use = in_total + out_total
        total_no_in_use = in_none + out_none

        accuracy = (tp + tn) / total_in_use if total_in_use > 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        asr = fp / blocked_total if blocked_total > 0 else 0

        print("\n======= Overall Metrics =======")
        print(f"Total Samples         : {total_samples}")
        print(f"--------------------------------")
        print(f" - Total used         : {total_in_use} (in+out populated)")
        print(f" - Total unused       : {total_no_in_use} (in+out none)")
        print(f"--------------------------------")
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


    def load_qa_for_system_tests_csv(self, filepath):
        qa_list = []
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines[1:]:  # Skip header
            line = line.strip()
            if not line:
                continue

            try:
                # Split CSV line safely assuming fields are enclosed in double quotes
                parts = [part.strip().strip('"').replace('""', '"') for part in line.split('","')]
                if len(parts) != 5:
                    print(f"Skipping malformed line (expected 5 columns): {line}")
                    continue

                questions = [q.strip() for q in parts[0].split("::")]
                q_statuses = [s.strip() for s in parts[1].split("::")]
                answers = [a.strip() for a in parts[2].split("::")]
                a_statuses = [s.strip() for s in parts[3].split("::")]
                category = [parts[4]]  # Do not split

                if not (len(questions) == len(q_statuses) == len(answers) == len(a_statuses)):
                    print(f"Skipping inconsistent line (mismatched counts): {line}")
                    continue

                qa_list.extend([questions, q_statuses, answers, a_statuses, category])

            except Exception as e:
                print(f"Error parsing line: {e}")
                continue

        return qa_list

    def generate_report(self, test_cases, overall_metrics_fn, output_path="system_test_report.md"):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        lines = ["# 🧪 System Test Report\n"]

        for test in test_cases:
            lines.append(f"## 📋 Test Case: `{test.name}`\n")
            for i, prompt in enumerate(test.in_prompts):
                lines.append(f"### 🔹 Sub-Test #{i + 1}")
                lines.append(f"- **Input Prompt**: `{prompt}`")
                lines.append(f"- **Expected Inbound Verdict**: `{test.expected_ins[i] if test.expected_ins else 'N/A'}`")
                lines.append(f"- **Actual Inbound Verdict**: `{test.inbound_dm_outputs[i].verdict if test.inbound_dm_outputs[i] else 'N/A'}`")
                lines.append(f"- **Inbound Filter Results**: `{test.inbound_filters_outputs[i]}`")
                lines.append(f"- **LLM Output**: `{test.llm_outputs[i]}`")
                lines.append(f"- **Expected Outbound Verdict**: `{test.expected_outs[i] if test.expected_outs else 'N/A'}`")
                lines.append(f"- **Actual Outbound Verdict**: `{test.outbound_dm_output[i].verdict if test.outbound_dm_output[i] else 'N/A'}`")
                lines.append(f"- **Outbound Filter Results**: `{test.outbound_filters_outputs[i]}`")
                lines.append(f"- ✅ **Partial Pass**: `{test.is_passed_partials[i]}`\n")

            lines.append(f"**➡️ Overall Pass for `{test.name}`: `{test.is_passed}`**\n")
            lines.append("---")

        # Capture print output from compute_overall_metrics
        metrics_output = io.StringIO()
        sys_stdout_backup = sys.stdout
        sys.stdout = metrics_output
        overall_metrics_fn(test_cases)
        sys.stdout = sys_stdout_backup

        lines.append("## 📊 Overall Metrics Summary\n")
        lines.append("```\n" + metrics_output.getvalue() + "\n```\n")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"✅ Report generated at: {os.path.abspath(output_path)}")