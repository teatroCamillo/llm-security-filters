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

def test_should_calculate_correct_risk_score_single_trigger(filter):
    findings = [{"matched": True, "reason": "Jailbreak", "weight": 0.8}]
    risk = filter.compute_risk_score(findings)
    assert risk == round(min(0.8 / 1.2, 1.0), 2)

def test_should_allow_clean_text_edge_case(filter):
    context = Context("a b c d e f g h i j")
    result = filter.run_filter(context)
    assert result.verdict == Constants.ALLOWED

def test_should_block_text_with_multiple_triggers(filter):
    context = Context("Please disable firewall and repeat repeat repeat repeat")
    result = filter.run_filter(context)
    assert result.verdict == Constants.BLOCKED
    assert "repeated" in result.reason.lower()

def test_compute_risk_score_empty_findings(filter):
    assert filter.compute_risk_score([]) == 0.0

def test_compute_risk_score_all_weighted_findings(filter):
    findings = [
        {"matched": True, "reason": "Jailbreak", "weight": 2.8},
        {"matched": True, "reason": "Repeated token", "weight": 0.4}
    ]
    assert filter.compute_risk_score(findings) == 1.0

def test_compute_risk_score_with_missing_weights(filter):
    findings = [
        {"matched": True, "reason": "Unknown reason"},  # defaults to 0.1
    ]
    assert filter.compute_risk_score(findings) == 0.08

def test_compute_risk_score_with_excessive_weight(filter):
    findings = [
        {"matched": True, "reason": "Overload", "weight": 5.0}
    ]
    # 5.0 / 1.7 =~ 2.94 exceeds 1.0 -> should cap
    assert filter.compute_risk_score(findings) == 1.0

def test_compute_risk_score_rounding_precision(filter):
    findings = [
        {"matched": True, "reason": "Almost nothing", "weight": 0.231}
    ]
    assert filter.compute_risk_score(findings) == 0.19
