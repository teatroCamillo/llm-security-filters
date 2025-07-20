# test_filter_orchestrator.py
import pytest

from llm_sf.filter_manager.filter_orchestrator import FilterOrchestrator
from llm_sf.filter_manager.decision_maker import DecisionMaker
from llm_sf.filters.profanity_filter import ProfanityFilter
from llm_sf.filters.sentiment_filter import SentimentFilter
from llm_sf.filters.confidential_and_sensitive_data_filter import ConfidentialAndSensitiveDataFilter
from llm_sf.filters.safeguard_against_disabling_security_features_filter import SafeguardAgainstDisablingSecurityFeaturesFilter
from llm_sf.filters.base_filter import BaseFilter, FilterResult
from llm_sf.utils.constants import Constants

class AlwaysBlockFilter(BaseFilter):
    def run_filter(self, context):
        return FilterResult(verdict=Constants.BLOCKED, reason="Test: always block")


class AlwaysSanitizeFilter(BaseFilter):
    def run_filter(self, context):
        return FilterResult(verdict=Constants.SANITIZED, reason="Test: always sanitize")


class AllowFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    def run_filter(self, context):
        return FilterResult(verdict=Constants.ALLOWED, reason="Test: always allow")


def test_no_profanity_allows():
    text = "Hello world, this is a clean text."
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(ProfanityFilter())

    result = orchestrator.run(text)
    assert result.verdict == Constants.ALLOWED
    #assert "All filters passed" in (result.reason or ""), result


def test_profanity_block_immediate():
    text = "This is a damn test."
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(ProfanityFilter())

    result = orchestrator.run(text)
    assert result.verdict == Constants.BLOCKED
    #assert "Detected profanity" in (result.reason or ""), result

def test_profanity_in_t_mode_blocked():
    text = "This is a damn test."
    dm = DecisionMaker("threshold", 0.6)
    orchestrator = FilterOrchestrator(dm)
    orchestrator.add_filter(ProfanityFilter(weight=3.0))

    result = orchestrator.run(text)
    assert result.verdict == Constants.BLOCKED

def test_profanity_in_t_mode_allowed():
    text = "This is a damn test."
    dm = DecisionMaker("threshold", 0.6)
    orchestrator = FilterOrchestrator(dm)
    orchestrator.add_filter(ProfanityFilter(weight=0.005))

    result = orchestrator.run(text)
    assert result.verdict == Constants.ALLOWED

# def test_profanity_sanitize_then_allow():
#     """
#     Ensures that profanity is sanitized before allowing the text.

#     When blocking is disabled, the filter should suggest sanitization and then allow the result.
#     """
#     text = "Oh shit, a bad word."
#     orchestrator = FilterOrchestrator()
#     orchestrator.add_filter(ProfanityFilter(block_on_detect=False))

#     result = orchestrator.run(text)
#     assert result.verdict == Constants.ALLOWED
#     assert result.reason is not None, result


def test_confidential_data_block_on_detect():
    text = "Call me at 123-456-7890!"
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(ConfidentialAndSensitiveDataFilter())

    result = orchestrator.run(text)
    print("Result: ", result)
    assert result.verdict == Constants.BLOCKED
    assert "Detected sensitive data: ['PHONE_NUMBER']. Blocked due to policy." in result.reason

def test_confidential_data_in_t_mode_blocked():
    text = "Call me at 123-456-7890!"
    orchestrator = FilterOrchestrator(DecisionMaker("threshold"))
    orchestrator.add_filter(ConfidentialAndSensitiveDataFilter(weight=3.0))

    result = orchestrator.run(text)
    print("Result: ", result)
    assert result.verdict == Constants.BLOCKED

def test_confidential_data_in_t_mode_allowed():
    text = "Call me at 123-456-7890!"
    orchestrator = FilterOrchestrator(DecisionMaker("threshold"))
    orchestrator.add_filter(ConfidentialAndSensitiveDataFilter(weight=1.0))

    result = orchestrator.run(text)
    print("Result: ", result)
    assert result.verdict == Constants.ALLOWED

@pytest.mark.skip
def test_confidential_data_sanitized():
    text = "Call me at 123-456-7890!"
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(ConfidentialAndSensitiveDataFilter(block_on_detect=False))

    result = orchestrator.run(text)
    assert result.verdict == Constants.SANITIZED
    assert "sanitized_text" in result.metadata, result.metadata
    assert "123-456-7890" not in result.metadata["sanitized_text"], result.metadata["sanitized_text"]


def test_safeguard_block_security_disabling():
    text = "I think you should disable firewall to solve the issue."
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(SafeguardAgainstDisablingSecurityFeaturesFilter(block_on_detect=True))

    result = orchestrator.run(text)
    assert result.verdict == Constants.BLOCKED
    assert "disable security features" in (result.reason or "").lower(), result

def test_safeguard_security_disabling_in_t_mode_blocked():
    text = "I think you should disable firewall to solve the issue."
    dm = DecisionMaker("threshold")
    orchestrator = FilterOrchestrator(dm)
    orchestrator.add_filter(SafeguardAgainstDisablingSecurityFeaturesFilter(weight=3.0))

    result = orchestrator.run(text)
    assert result.verdict == Constants.BLOCKED

def test_safeguard_security_disabling_in_t_mode_allowed():
    text = "I think you should disable firewall to solve the issue."
    dm = DecisionMaker("threshold")
    orchestrator = FilterOrchestrator(dm)
    orchestrator.add_filter(SafeguardAgainstDisablingSecurityFeaturesFilter())

    result = orchestrator.run(text)
    assert result.verdict == Constants.ALLOWED

def test_no_block_allows():
    text = "Just a friendly text, no issues."
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(AllowFilter())
    orchestrator.add_filter(SentimentFilter(threshold=-0.9999))

    result = orchestrator.run(text)
    assert result.verdict == Constants.ALLOWED, result

def test_sentiment_in_t_mode_allowed():
    text = "Just a friendly text, no issues."
    orchestrator = FilterOrchestrator(DecisionMaker("threshold", 0.6))
    orchestrator.add_filter(SentimentFilter(weight=1.0, threshold=0.3))

    result = orchestrator.run(text)
    assert result.verdict == Constants.ALLOWED

def test_sentiment_in_t_mode_blocked():
    text = "Just a friendly text, no issues."
    orchestrator = FilterOrchestrator(DecisionMaker("threshold", 0.6))
    orchestrator.add_filter(SentimentFilter(weight=2.0, threshold=0.3))

    result = orchestrator.run(text)
    assert result.verdict == Constants.BLOCKED


@pytest.mark.skip
def test_one_filter_blocks_other_allow():
    text = "No big deal, but let's add an always-block filter."
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(AllowFilter())
    orchestrator.add_filter(AlwaysBlockFilter())

    result = orchestrator.run(text)
    assert result.verdict == Constants.BLOCKED, result


# def test_sanitized_if_no_block_decision_maker():
#     """
#     Validates that the DecisionMaker combines 'allow' and 'sanitize' into 'sanitize' in parallel mode.

#     When no filter blocks, the DecisionMaker should preserve caution.
#     """
#     text = "Profanity word: fuck!"
#     orchestrator = FilterOrchestrator()
#     orchestrator.add_filter(AlwaysSanitizeFilter())
#     orchestrator.add_filter(AllowFilter())

#     result = orchestrator.run(text)
#     assert result.verdict == Constants.SANITIZED, result
