# test_filter_orchestrator.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest

from filter_manager.filter_orchestrator import FilterOrchestrator
from filters.profanity_filter import ProfanityFilter
from filters.sentiment_filter import SentimentFilter
from filters.confidential_and_sensitive_data_filter import ConfidentialAndSensitiveDataFilter
from filters.safeguard_against_disabling_security_features_filter import SafeguardAgainstDisablingSecurityFeaturesFilter
from filters.base_filter import BaseFilter, FilterResult


class AlwaysBlockFilter(BaseFilter):
    """
    Testowy filtr, który zawsze zwraca "block".
    """
    def run_filter(self, context):
        return FilterResult(verdict="block", reason="Test: always block")


class AlwaysSanitizeFilter(BaseFilter):
    """
    Testowy filtr, który zawsze zwraca "sanitize",
    ale nigdy nie podaje gotowego sanitized_text.
    """
    def run_filter(self, context):
        return FilterResult(verdict="sanitize", reason="Test: always sanitize")


class AllowFilter(BaseFilter):
    """
    Testowy filtr, który zawsze przepuszcza (allow).
    """
    def run_filter(self, context):
        return FilterResult(verdict="allow", reason="Test: always allow")


def test_serial_no_profanity_allows():
    """
    W trybie serial, gdy nie ma wulgaryzmów, finalnie ma być 'allow'.
    """
    text = "Hello world, this is a clean text."
    orchestrator = FilterOrchestrator().apply(mode="serial")
    orchestrator.add_filter(ProfanityFilter(block_on_detect=True))

    result = orchestrator.run(text)
    assert result.verdict == "allow"
    assert "All filters passed" in (result.reason or ""), result


def test_serial_profanity_block_immediate():
    """
    Gdy ProfanityFilter ma block_on_detect=True i tekst zawiera wulgaryzm, 
    oczekujemy natychmiastowego 'block' w trybie serial.
    """
    text = "This is a damn test."
    orchestrator = FilterOrchestrator().apply(mode="serial")
    orchestrator.add_filter(ProfanityFilter(block_on_detect=True))

    result = orchestrator.run(text)
    assert result.verdict == "block"
    assert "Detected profanity" in (result.reason or ""), result


def test_serial_profanity_sanitize_then_allow():
    """
    Gdy ProfanityFilter ma block_on_detect=False i tekst zawiera wulgaryzmy,
    filtr zasugeruje 'sanitize'. Orkiestrator powinien wywołać DataSanitizer,
    a następnie ponownie sprawdzić filtr - w końcu 'allow'.
    """
    text = "Oh shit, a bad word."
    orchestrator = FilterOrchestrator(max_sanitize_attempts=2).apply(mode="serial")
    orchestrator.add_filter(ProfanityFilter(block_on_detect=False))

    result = orchestrator.run(text)
    assert result.verdict == "allow"
    # Sprawdzamy, czy reason nie jest pusty
    assert result.reason is not None, result


def test_serial_confidential_data_block_on_detect():
    """
    Tekst zawiera np. numer telefonu. Filtr poufny z block_on_detect=True -> 'block'.
    """
    text = "Call me at 123-456-7890!"
    orchestrator = FilterOrchestrator().apply("serial")
    orchestrator.add_filter(ConfidentialAndSensitiveDataFilter(block_on_detect=True))

    result = orchestrator.run(text)
    assert result.verdict == "block"
    assert "Detected confidential/sensitive data" in (result.reason or ""), result


def test_serial_confidential_data_sanitize_then_allow():
    """
    Numer telefonu, ale block_on_detect=False -> najpierw 'sanitize', 
    po poprawieniu finalnie 'allow'.
    """
    text = "Call me at 123-456-7890!"
    orchestrator = FilterOrchestrator(max_sanitize_attempts=1).apply("serial")
    orchestrator.add_filter(ConfidentialAndSensitiveDataFilter(block_on_detect=False))

    result = orchestrator.run(text)
    assert result.verdict == "allow"
    assert "final_text" in result.metadata, result.metadata
    assert "123-456-7890" not in result.metadata["final_text"], result.metadata["final_text"]


def test_serial_safeguard_block_security_disabling():
    """
    SafeguardAgainstDisablingSecurityFeaturesFilter -> block_on_detect=True
    Jeśli w tekście jest fraza 'disable firewall', spodziewamy się 'block'.
    """
    text = "I think you should disable firewall to solve the issue."
    orchestrator = FilterOrchestrator().apply("serial")
    orchestrator.add_filter(SafeguardAgainstDisablingSecurityFeaturesFilter(block_on_detect=True))

    result = orchestrator.run(text)
    assert result.verdict == "block"
    assert "disable security features" in (result.reason or "").lower(), result


def test_serial_max_sanitize_attempts_exceeded():
    """
    Filtr, który zawsze zwraca 'sanitize' i nigdy nie poprawia tekstu.
    Po przekroczeniu max_sanitize_attempts -> 'block'.
    """
    text = "some text"
    orchestrator = FilterOrchestrator(max_sanitize_attempts=2).apply(mode="serial")
    orchestrator.add_filter(AlwaysSanitizeFilter())

    result = orchestrator.run(text)
    assert result.verdict == "block"
    assert "Exceeded max_sanitize_attempts" in (result.reason or ""), result


def test_parallel_no_block_allows():
    """
    W trybie parallel mamy filtry, które nie blokują; finalnie 'allow'.
    """
    text = "Just a friendly text, no issues."
    orchestrator = FilterOrchestrator().apply(mode="parallel")
    orchestrator.add_filter(AllowFilter())
    # SentimentFilter: ustalamy threshold bardzo nisko, 
    # by 'allow' nawet dla negatywnych. 
    orchestrator.add_filter(SentimentFilter(threshold=-0.9999, block_on_negative=True))

    result = orchestrator.run(text)
    assert result.verdict == "allow", result


def test_parallel_one_filter_blocks_others_allow():
    """
    W trybie równoległym jeden filtr zwraca 'block', drugi 'allow'. 
    Efekt końcowy: 'block'.
    """
    text = "No big deal, but let's add an always-block filter."
    orchestrator = FilterOrchestrator().apply(mode="parallel")
    orchestrator.add_filter(AllowFilter())
    orchestrator.add_filter(AlwaysBlockFilter())

    result = orchestrator.run(text)
    assert result.verdict == "block", result


def test_parallel_sanitize_if_no_block_decision_maker():
    """
    Tryb równoległy z DM: 
    - Jeden filtr zgłasza 'sanitize'
    - Drugi filtr zgłasza 'allow'
    - Żaden nie blokuje
    Decision Maker powinien połączyć to w final 'sanitize'.
    """
    text = "Profanity word: fuck!"
    orchestrator = FilterOrchestrator(max_sanitize_attempts=2).apply("parallel").dm()
    orchestrator.add_filter(AlwaysSanitizeFilter())
    orchestrator.add_filter(AllowFilter())

    result = orchestrator.run(text)
    assert result.verdict == "sanitize", result
