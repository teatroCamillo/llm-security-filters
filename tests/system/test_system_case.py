from llm_sf.utils.constants import Constants

class SystemTestCase:
    def __init__(self, prompts, expected_in=None, expected_out=None, name=None):
        self.name = name or "UnnamedTest"
        self.prompts = prompts
        self.expected_in = expected_in
        self.expected_out = expected_out

        # Results tracking
        self.inbound_final_output = None
        self.inbound_filters_outputs = []    # List[FilterResult]
        self.llm_outputs = []               # List[str]
        self.outbound_final_output = None
        self.outbound_filters_outputs = []   # List[FilterResult]
        self.result = None                   # T/F both (in & out) passed?
