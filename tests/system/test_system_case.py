from llm_sf.utils.constants import Constants

class SystemTestCase:
    def __init__(self, prompts, expected_behavior, name=None):
        self.name = name or "UnnamedTest"
        self.prompts = prompts
        self.expected = expected_behavior

        # Results tracking
        self.inbound_filter_outputs = []    # List[FilterResult]
        self.outbound_filter_outputs = []   # List[FilterResult]
        self.llm_outputs = []               # List[str]
        self.actual_behaviors = []          # Final decision: ALLOWED, BLOCKED, SANITIZED
        self.results = []                   # Pass/fail list

    def run(self, call_llm_fn, inbound_orchestrator=None, outbound_orchestrator=None):
        for prompt in self.prompts:
            if inbound_orchestrator:
                inbound_result = inbound_orchestrator.run(prompt)
                self.inbound_filter_outputs.append(inbound_result)

                if inbound_result.verdict == Constants.BLOCKED:
                    self.llm_outputs.append(None)
                    self.outbound_filter_outputs.append(None)
                    self.actual_behaviors.append(Constants.BLOCKED)
                    self.results.append(Constants.BLOCKED == self.expected)
                    continue

                if inbound_result.verdict == Constants.SANITIZED:
                    user_input_filtered = inbound_result.metadata.get("sanitized_text", "")
                else:
                    user_input_filtered = inbound_result.metadata.get("final_text", "")
            else:
                # No inbound filtering, use original prompt
                self.inbound_filter_outputs.append(None)
                user_input_filtered = prompt

            conversation = [{"role": "user", "content": user_input_filtered}]
            llm_output = call_llm_fn(conversation)
            self.llm_outputs.append(llm_output)

            if outbound_orchestrator:
                outbound_result = outbound_orchestrator.run(llm_output)
                self.outbound_filter_outputs.append(outbound_result)

                if outbound_result.verdict == Constants.BLOCKED:
                    self.actual_behaviors.append(Constants.BLOCKED)
                elif outbound_result.verdict == Constants.SANITIZED:
                    self.actual_behaviors.append(Constants.SANITIZED)
                else:
                    self.actual_behaviors.append(Constants.ALLOWED)
            else:
                self.outbound_filter_outputs.append(None)
                self.actual_behaviors.append(Constants.ALLOWED)

            self.results.append(self.actual_behaviors[-1] == self.expected)
