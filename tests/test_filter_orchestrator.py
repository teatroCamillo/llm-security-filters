# test_filter_orchestrator.py
import pytest

from llm_sf.filter_manager.filter_orchestrator import FilterOrchestrator
from llm_sf.filters.profanity_filter import ProfanityFilter
from llm_sf.filters.sentiment_filter import SentimentFilter
from llm_sf.filters.confidential_and_sensitive_data_filter import ConfidentialAndSensitiveDataFilter
from llm_sf.filters.safeguard_against_disabling_security_features_filter import SafeguardAgainstDisablingSecurityFeaturesFilter
from llm_sf.filters.base_filter import BaseFilter, FilterResult


class AlwaysBlockFilter(BaseFilter):
    """A test filter that always returns a 'block' verdict."""
    def run_filter(self, context):
        return FilterResult(verdict="block", reason="Test: always block")


class AlwaysSanitizeFilter(BaseFilter):
    """
    A test filter that always returns 'sanitize', but does not include a sanitized version.

    Used to simulate repeated sanitization cycles that never succeed.
    """
    def run_filter(self, context):
        return FilterResult(verdict="sanitized", reason="Test: always sanitize")


class AllowFilter(BaseFilter):
    """A test filter that always returns 'allow' verdict unconditionally."""
    def run_filter(self, context):
        return FilterResult(verdict="allow", reason="Test: always allow")


def test_no_profanity_allows():
    text = "Hello world, this is a clean text."
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(ProfanityFilter())

    result = orchestrator.run(text)
    assert result.verdict == "allow"
    #assert "All filters passed" in (result.reason or ""), result


def test_profanity_block_immediate():
    text = "This is a damn test."
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(ProfanityFilter())

    result = orchestrator.run(text)
    assert result.verdict == "block"
    #assert "Detected profanity" in (result.reason or ""), result


# def test_profanity_sanitize_then_allow():
#     """
#     Ensures that profanity is sanitized before allowing the text.

#     When blocking is disabled, the filter should suggest sanitization and then allow the result.
#     """
#     text = "Oh shit, a bad word."
#     orchestrator = FilterOrchestrator()
#     orchestrator.add_filter(ProfanityFilter(block_on_detect=False))

#     result = orchestrator.run(text)
#     assert result.verdict == "allow"
#     assert result.reason is not None, result


def test_confidential_data_block_on_detect():
    """
    Verifies that sensitive data (e.g., phone number) is blocked if the filter is configured to block.

    The ConfidentialAndSensitiveDataFilter should return 'block' on detection.
    """
    text = "Call me at 123-456-7890!"
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(ConfidentialAndSensitiveDataFilter())

    result = orchestrator.run(text)
    print("Result: ", result)
    assert result.verdict == "block"
    assert "Detected sensitive data: ['PHONE_NUMBER']. Blocked due to policy." in result.reason

@pytest.mark.skip
def test_confidential_data_sanitized():
    """
    Ensures that sensitive data is sanitized when blocking is disabled.

    Final result should be 'allow' with redacted output.
    """
    text = "Call me at 123-456-7890!"
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(ConfidentialAndSensitiveDataFilter(block_on_detect=False))

    result = orchestrator.run(text)
    assert result.verdict == "sanitized"
    assert "sanitized_text" in result.metadata, result.metadata
    assert "123-456-7890" not in result.metadata["sanitized_text"], result.metadata["sanitized_text"]


def test_safeguard_block_security_disabling():
    """
    Validates that disabling security-related features leads to a block verdict.

    This ensures the safeguard filter blocks phrases like 'disable firewall'.
    """
    text = "I think you should disable firewall to solve the issue."
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(SafeguardAgainstDisablingSecurityFeaturesFilter(block_on_detect=True))

    result = orchestrator.run(text)
    assert result.verdict == "block"
    assert "disable security features" in (result.reason or "").lower(), result

def test_no_block_allows():
    """
    Ensures that when no filter returns 'block' in parallel mode, the final verdict is 'allow'.

    Filters are configured to allow or return low-impact results.
    """
    text = "Just a friendly text, no issues."
    orchestrator = FilterOrchestrator()
    orchestrator.add_filter(AllowFilter())
    orchestrator.add_filter(SentimentFilter(threshold=-0.9999))

    result = orchestrator.run(text)
    assert result.verdict == "allow", result

@pytest.mark.skip
def test_one_filter_blocks_other_allow():
    """
    Ensures that in parallel mode, even one blocking filter results in a final 'block' verdict.

    Other filters may allow, but 'block' takes precedence.
    """
    text = "No big deal, but let's add an always-block filter."
    orchestrator = FilterOrchestrator(mode="parallel")
    orchestrator.add_filter(AllowFilter())
    orchestrator.add_filter(AlwaysBlockFilter())

    result = orchestrator.run(text)
    assert result.verdict == "block", result


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
#     assert result.verdict == "sanitize", result
