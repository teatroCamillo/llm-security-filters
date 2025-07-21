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
        self.actual_behaviors = []          # Final decision: ALLOWED, BLOCKED
        self.results = []                   # Pass/fail list
