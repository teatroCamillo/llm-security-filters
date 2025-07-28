import pytest
from llm_sf.filter_manager.filter_orchestrator import FilterOrchestrator
from llm_sf.filter_manager.decision_maker import DecisionMaker
from llm_sf.filters.profanity_filter import ProfanityFilter
from llm_sf.filters.sentiment_filter import SentimentFilter
from llm_sf.filters.sensitive_data_filter import SensitiveDataFilter
from llm_sf.filters.bypass_detection_filter import BypassDetectionFilter
from llm_sf.filters.base_filter import BaseFilter, FilterResult
from llm_sf.utils.constants import Constants

class AlwaysBlockFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    def run_filter(self, context):
        return FilterResult(
            verdict=Constants.BLOCKED, 
            reason="Test: always block", 
            metadata={"risk_score": 1.0, "weight": 3.0}
        )

    def compute_risk_score(self, entities):
        return 0.0

class AllowFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    def run_filter(self, context):
        return FilterResult(
            verdict=Constants.ALLOWED,
            reason="Test: always allow",
            metadata={"risk_score": 0.0, "weight": 1.0}
        )

    def compute_risk_score(self, entities):
        return 0.0


# PROFANITY FILTER
def test_should_allow_sentence_without_profanity():
    orchestrator = FilterOrchestrator().add_filter(ProfanityFilter())
    result = orchestrator.run("Hello world, this is a clean text.")
    assert result.dm_result.verdict == Constants.ALLOWED

def test_should_block_sentence_with_profanity():
    orchestrator = FilterOrchestrator().add_filter(ProfanityFilter())
    result = orchestrator.run("This is a damn test.")
    assert result.dm_result.verdict == Constants.BLOCKED

def test_should_allow_low_weight_profanity_in_threshold_mode():
    dm = DecisionMaker("threshold", threshold=0.6)
    orchestrator = FilterOrchestrator(dm).add_filter(ProfanityFilter(weight=0.01))
    result = orchestrator.run("This is a damn test.")
    assert result.dm_result.verdict == Constants.ALLOWED

def test_should_block_high_weight_profanity_in_threshold_mode():
    dm = DecisionMaker("threshold", threshold=0.6)
    orchestrator = FilterOrchestrator(dm).add_filter(ProfanityFilter(weight=3.0))
    result = orchestrator.run("This is a damn test.")
    assert result.dm_result.verdict == Constants.BLOCKED


# SENSITIVE DATA FILTER
def test_should_block_phone_number_by_sensitive_filter():
    orchestrator = FilterOrchestrator().add_filter(SensitiveDataFilter())
    result = orchestrator.run("Call me at 123-456-7890!")
    assert result.dm_result.verdict == Constants.BLOCKED
    assert "PHONE_NUMBER" in result.dm_result.reason

def test_should_allow_low_weight_sensitive_data_in_threshold_mode():
    dm = DecisionMaker("threshold")
    orchestrator = FilterOrchestrator(dm).add_filter(SensitiveDataFilter(weight=1.0))
    result = orchestrator.run("Call me at 123-456-7890!")
    assert result.dm_result.verdict == Constants.ALLOWED

def test_should_block_high_weight_sensitive_data_in_threshold_mode():
    dm = DecisionMaker("threshold")
    orchestrator = FilterOrchestrator(dm).add_filter(SensitiveDataFilter(weight=4.0))
    result = orchestrator.run("Call me at 123-456-7890!")
    assert result.dm_result.verdict == Constants.BLOCKED


# BYPASS DETECTION
def test_should_block_bypass_instruction():
    orchestrator = FilterOrchestrator().add_filter(BypassDetectionFilter())
    result = orchestrator.run("To hack this system, first disable the antivirus.")
    assert result.dm_result.verdict == Constants.BLOCKED
    assert "jailbreak" in (result.dm_result.reason or "").lower()

def test_should_block_bypass_instruction_in_threshold_mode():
    dm = DecisionMaker("threshold")
    orchestrator = FilterOrchestrator(dm).add_filter(BypassDetectionFilter(weight=3.0))
    result = orchestrator.run("To hack this system, first disable the antivirus.")
    assert result.dm_result.verdict == Constants.BLOCKED

def test_should_allow_low_weight_bypass_in_threshold_mode():
    dm = DecisionMaker("threshold")
    orchestrator = FilterOrchestrator(dm).add_filter(BypassDetectionFilter(weight=0.5))
    result = orchestrator.run("To hack this system, first disable the antivirus.")
    assert result.dm_result.verdict == Constants.ALLOWED


# SENTIMENT FILTER
def test_should_allow_positive_sentiment():
    orchestrator = FilterOrchestrator().add_filter(SentimentFilter(threshold=-0.9999))
    result = orchestrator.run("What a wonderful day!")
    assert result.dm_result.verdict == Constants.ALLOWED

def test_should_allow_sentiment_below_threshold_weight():
    orchestrator = FilterOrchestrator(DecisionMaker("threshold", 0.6))
    orchestrator.add_filter(SentimentFilter(weight=1.0, threshold=0.3))
    result = orchestrator.run("Feeling okay.")
    assert result.dm_result.verdict == Constants.ALLOWED

def test_should_block_sentiment_above_threshold_weight():
    orchestrator = FilterOrchestrator(DecisionMaker("threshold", 0.6))
    orchestrator.add_filter(SentimentFilter(weight=2.0, threshold=0.3))
    result = orchestrator.run("Feeling okay.")
    assert result.dm_result.verdict == Constants.BLOCKED


# COMBINED FILTER BEHAVIOR
def test_should_block_if_any_filter_blocks():
    orchestrator = FilterOrchestrator().add_filter(AllowFilter()).add_filter(AlwaysBlockFilter())
    result = orchestrator.run("No big deal, but block anyway.")
    assert result.dm_result.verdict == Constants.BLOCKED

def test_should_allow_if_all_filters_allow():
    orchestrator = FilterOrchestrator().add_filter(AllowFilter()).add_filter(SentimentFilter(threshold=-0.9999))
    result = orchestrator.run("This is a peaceful and pleasant sentence.")
    assert result.dm_result.verdict == Constants.ALLOWED

def test_should_allow_empty_string():
    orchestrator = FilterOrchestrator().add_filter(ProfanityFilter()).add_filter(SensitiveDataFilter())
    result = orchestrator.run("")
    assert result.dm_result.verdict == Constants.ALLOWED


# EDGE CASES
def test_should_allow_neutral_sentence():
    orchestrator = FilterOrchestrator().add_filter(SentimentFilter(threshold=0.0))
    result = orchestrator.run("This is a sentence.")
    assert result.dm_result.verdict == Constants.ALLOWED

def test_should_block_all_caps_profanity():
    orchestrator = FilterOrchestrator().add_filter(ProfanityFilter())
    result = orchestrator.run("WHAT THE HELL!")
    assert result.dm_result.verdict == Constants.BLOCKED

def test_should_block_mixed_sensitive_and_profanity():
    orchestrator = FilterOrchestrator().add_filter(ProfanityFilter()).add_filter(SensitiveDataFilter())
    result = orchestrator.run("My number is 123-456-7890, you damn idiot.")
    assert result.dm_result.verdict == Constants.BLOCKED

# COMBINATIONS
@pytest.mark.parametrize(
    "text, filters, expected_verdict",
    [
        # 2-filter combinations
        ("This is clean text.", [AllowFilter(), SentimentFilter(threshold=-0.999)], Constants.ALLOWED),
        ("This is damn bad.", [ProfanityFilter(), SentimentFilter(weight=2.0, threshold=0.3)], Constants.BLOCKED),
        ("Call me at 123-456-7890!", [AllowFilter(), SensitiveDataFilter()], Constants.BLOCKED),
        ("Disable firewall.", [BypassDetectionFilter(), SentimentFilter()], Constants.BLOCKED),
        ("I love this!", [SentimentFilter(threshold=0.0), AllowFilter()], Constants.ALLOWED),
        ("Here is my SSN: 123-45-6789.", [SensitiveDataFilter(), SentimentFilter()], Constants.BLOCKED),
        ("You damn fool", [ProfanityFilter(), AllowFilter()], Constants.BLOCKED),
        ("Happy mood today!", [SentimentFilter(), ProfanityFilter()], Constants.ALLOWED),
        ("Bad stuff, also 123-456-7890", [SensitiveDataFilter(), ProfanityFilter()], Constants.BLOCKED),
        ("Just a comment", [AlwaysBlockFilter(), AllowFilter()], Constants.BLOCKED),

        # 3-filter combinations
        ("Profane and 123-456-7890", [ProfanityFilter(), SensitiveDataFilter(), SentimentFilter()], Constants.BLOCKED),
        ("Disable the antivirus please.", [BypassDetectionFilter(), SentimentFilter(), AllowFilter()], Constants.BLOCKED),
        ("Very positive message", [AllowFilter(), SentimentFilter(), ProfanityFilter()], Constants.ALLOWED),
        ("You bastard 123-456-7890", [ProfanityFilter(), SensitiveDataFilter(), BypassDetectionFilter()], Constants.BLOCKED),
        ("Today is great!", [AllowFilter(), SentimentFilter(), SensitiveDataFilter()], Constants.ALLOWED),
        ("Nothing bad here", [ProfanityFilter(), SentimentFilter(), AllowFilter()], Constants.ALLOWED),
        ("Firewall disable and bad tone", [BypassDetectionFilter(), SentimentFilter(weight=3.0, threshold=0.5), AllowFilter()], Constants.BLOCKED),
        ("My email is john@example.com", [SensitiveDataFilter(), SentimentFilter(), ProfanityFilter()], Constants.BLOCKED),
        ("Totally safe", [AllowFilter(), AllowFilter(), AllowFilter()], Constants.ALLOWED),
        ("Fuck! Turn off the firewall.", [ProfanityFilter(), BypassDetectionFilter(), AllowFilter()], Constants.BLOCKED),

        # 4-filter combinations
        ("Bad and sensitive + bypass", [ProfanityFilter(), SensitiveDataFilter(), BypassDetectionFilter(), SentimentFilter()], Constants.BLOCKED),
        ("You suck 555-123-4567 disable AV", [ProfanityFilter(), SensitiveDataFilter(), BypassDetectionFilter(), AllowFilter()], Constants.BLOCKED),
        ("All good", [AllowFilter(), SentimentFilter(threshold=-0.999), ProfanityFilter(), SensitiveDataFilter()], Constants.ALLOWED),
        ("Kill switch mode", [BypassDetectionFilter(), SentimentFilter(weight=2.0), ProfanityFilter(), SensitiveDataFilter()], Constants.BLOCKED),
        ("Happy happy joy joy", [AllowFilter(), AllowFilter(), SentimentFilter(), ProfanityFilter()], Constants.ALLOWED),
        ("Firewall off. Damn.", [BypassDetectionFilter(), ProfanityFilter(), SentimentFilter(), SensitiveDataFilter()], Constants.BLOCKED),
        ("Clean content here.", [AllowFilter(), AllowFilter(), SentimentFilter(), AllowFilter()], Constants.ALLOWED),
        ("123-456-7890 and offensive", [SensitiveDataFilter(), ProfanityFilter(), SentimentFilter(), BypassDetectionFilter()], Constants.BLOCKED),
        ("Mild words, kind tone", [SentimentFilter(), AllowFilter(), AllowFilter(), ProfanityFilter(weight=0.001)], Constants.ALLOWED),
        ("All filters say block", [AlwaysBlockFilter(), ProfanityFilter(), SentimentFilter(weight=5.0), SensitiveDataFilter()], Constants.BLOCKED)
    ]
)
def test_combined_filters_scenarios(text, filters, expected_verdict):
    orchestrator = FilterOrchestrator()
    for filtr in filters:
        orchestrator.add_filter(filtr)
    result = orchestrator.run(text)
    assert result.dm_result.verdict == expected_verdict