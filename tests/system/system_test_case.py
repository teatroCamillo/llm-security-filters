from llm_sf.utils.constants import Constants

class SystemTestCase:
    def __init__(self, in_prompts=[], out_prompts=[], expected_ins=[], expected_outs=[], name=None):
        self.name = name or "UnnamedTest"
        self.in_prompts = in_prompts
        self.out_prompts = out_prompts
        self.expected_ins = expected_ins
        self.expected_outs = expected_outs

        # Results tracking
        self.inbound_dm_outputs = []
        self.inbound_filters_outputs = []    # List[FilterResult]
        self.llm_outputs = []               # List[str]
        self.outbound_dm_output = []
        self.outbound_filters_outputs = []   # List[FilterResult]
        self.is_passed_partials = []          
        self.is_passed = None       # T/F both (in & out) passed?

    def __str__(self):
        return (
            f"SystemTestCase(name={self.name!r}, "
            f"in_prompts={self.in_prompts!r}, "
            f"out_prompts={self.out_prompts!r}, "
            f"expected_ins={self.expected_ins!r}, "
            f"expected_outs={self.expected_outs!r}, "
            f"is_passed_partials={self.is_passed_partials!r}, "
            f"is_passed={self.is_passed!r})"
        )