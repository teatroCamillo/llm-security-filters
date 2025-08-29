# test_bypass_detection_filter.py
import pytest
from llm_sf.filters.bypass_detection_filter import BypassDetectionFilter
from llm_sf.filter_manager.context import Context
from llm_sf.utils.constants import Constants

def test_should_initialize_with_default_weight():
    filter_instance = BypassDetectionFilter()
    assert filter_instance.weight == 1.0

def test_should_initialize_with_valid_weight():
    filter_instance = BypassDetectionFilter(weight=7.3)
    assert filter_instance.weight == 7.3

@pytest.mark.parametrize("invalid_weight", [-0.01, -10, 10.01, 100])
def test_should_raise_error_for_weight_out_of_bounds(invalid_weight):
    with pytest.raises(ValueError, match="Weight must be between 0.0 and 10.0"):
        BypassDetectionFilter(weight=invalid_weight)

@pytest.mark.parametrize("boundary_weight", [0.0, 10.0])
def test_should_allow_weight_at_boundary_values(boundary_weight):
    filter_instance = BypassDetectionFilter(weight=boundary_weight)
    assert filter_instance.weight == boundary_weight

@pytest.fixture
def filter():
    return BypassDetectionFilter()

@pytest.mark.parametrize("sentence", Constants.load_csv(Constants.CLEAN_SENTENCES_FULL_CSV))
def test_should_allow_clean_sentence(sentence, filter):
    context = Context(sentence)
    result = filter.run_filter(context)
    assert result.verdict == Constants.ALLOWED

@pytest.mark.parametrize("prompt", Constants.load_csv(Constants.JAILBREAK_PROMPTS_CSV))
def test_should_block_due_to_jailbreak_patterns(prompt, filter):
    context = Context(prompt)
    result = filter.run_filter(context)
    if result.verdict == Constants.ALLOWED:
        print(prompt)
    assert result.verdict == Constants.BLOCKED
    assert "jailbreak" in result.reason.lower() or "pattern" in result.reason.lower()

@pytest.mark.parametrize("sentence", [
    "help help help help",
    "please please please please assist",
])
def test_should_block_due_to_repeated_tokens(sentence, filter):
    context = Context(sentence)
    result = filter.run_filter(context)
    assert result.verdict == Constants.BLOCKED
    assert "repeated" in result.reason.lower()

def test_should_allow_short_random_string(filter):
    context = Context("A1B2")
    result = filter.run_filter(context)
    assert result.verdict == Constants.ALLOWED

def test_should_allow_clean_text_edge_case(filter):
    context = Context("a b c d e f g h i j")
    result = filter.run_filter(context)
    assert result.verdict == Constants.ALLOWED

def test_should_block_text_with_multiple_triggers(filter):
    context = Context("Please disable firewall and repeat repeat repeat repeat")
    result = filter.run_filter(context)
    assert result.verdict == Constants.BLOCKED
    assert "repeated" in result.reason.lower()

@pytest.mark.parametrize("findings, expected", [
    # Empty or invalid
    ([], 0.0),
    ([{}], 0.0),
    ([{"weight": -1.0}], 0.0),
    ([{"weight": 100.0}], 1.0),

    # Single findings
    ([{"weight": 1.0}], 0.38),
    ([{"weight": 5.0}], 0.84),
    ([{"weight": 10.0}], 1.0),

    # Multiple same-weight
    ([{"weight": 1.0}] * 5, 0.92),  # (0.1 * 0.6) + (0.5 * 0.4)
    ([{"weight": 10.0}] * 10, 1.0),
    ([{"weight": 5.0}] * 10, 1.0),
    ([{"weight": 5.0}] * 20, 1.0),  # Count factor capped at 1.0

    # Mixed weights
    ([{"weight": 2.0}, {"weight": 4.0}], 0.9),
    ([{"weight": 0.0}, {"weight": 10.0}], 1.0),

    # Count dominated
    ([{"weight": 1.0}] * 10, 1.0),
    ([{"weight": 1.0}] * 5, 0.92),
    ([{"weight": 1.0}] * 20, 1.0),

    # Weight dominated
    ([{"weight": 10.0}], 1.0),
    ([{"weight": 10.0}, {"weight": 10.0}], 1.0),

    # Realistic mixes
    ([{"weight": 0.5}, {"weight": 1.5}, {"weight": 2.0}], 0.8),
    ([{"weight": 9.0}, {"weight": 0.0}, {"weight": 1.0}], 1.0),
    ([{"weight": 5.0}, {"weight": 5.0}, {"weight": 5.0}], 1.0),

    # With missing or bad data
    ([{"weight": 0.5}, {}, {"weight": 0.5}], 0.48),
    ([{}, {}, {"weight": 10.0}], 1.0),
])
def test_compute_risk_score(findings, expected, filter):
    assert filter.compute_risk_score(findings) == expected