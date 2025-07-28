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
