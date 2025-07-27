# test_bypass_detection_filter.py
import pytest
from llm_sf.filters.bypass_detection_filter import BypassDetectionFilter
from llm_sf.filter_manager.context import Context
from llm_sf.utils.constants import Constants

@pytest.fixture
def filter():
    return BypassDetectionFilter()

@pytest.mark.parametrize("sentence", Constants.load_clean_sentences())
def test_should_allow_clean_sentence(sentence, filter):
    context = Context(sentence)
    result = filter.run_filter(context)
    assert result.verdict == Constants.ALLOWED

# @pytest.mark.parametrize("prompt", Constants.load_jailbreak_prompts())
# def test_should_block_due_to_jailbreak_patterns(prompt, filter):
#     context = Context(prompt)
#     result = filter.run_filter(context)
#     if result.verdict == Constants.ALLOWED:
#         print(prompt)
#     assert result.verdict == Constants.BLOCKED
#     assert "jailbreak" in result.reason.lower() or "pattern" in result.reason.lower()

# @pytest.mark.parametrize("sentence", [
#     "help help help help",
#     "please please please please assist",
# ])
# def test_should_block_due_to_repeated_tokens(sentence, filter):
#     context = Context(sentence)
#     result = filter.run_filter(context)
#     assert result.verdict == Constants.BLOCKED
#     assert "repeated" in result.reason.lower()

# @pytest.mark.parametrize("sentence", [
#     "Q: What’s 2 + 2? A: 4. Q: Capital of France? A: Paris.",
#     "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6",
# ])
# def test_should_block_due_to_high_entropy(sentence, filter):
#     context = Context(sentence)
#     result = filter.run_filter(context)
#     assert result.verdict == Constants.BLOCKED
#     assert "entropy" in result.reason.lower()

# def test_should_allow_short_random_string(filter):
#     context = Context("A1B2")
#     result = filter.run_filter(context)
#     assert result.verdict == Constants.ALLOWED

# def test_should_calculate_correct_risk_score_single_trigger(filter):
#     findings = [{"matched": True, "reason": "Jailbreak", "weight": 0.8}]
#     risk = filter.compute_risk_score(findings)
#     assert risk == round(min(0.8 / 1.7, 1.0), 2)

# def test_should_allow_clean_text_edge_case(filter):
#     context = Context("a b c d e f g h i j")
#     result = filter.run_filter(context)
#     assert result.verdict == Constants.ALLOWED

# def test_should_block_text_with_multiple_triggers(filter):
#     context = Context("Please disable firewall and repeat repeat repeat repeat")
#     result = filter.run_filter(context)
#     assert result.verdict == Constants.BLOCKED
#     assert "repeated" in result.reason.lower()

# def test_should_calculate_max_risk_score(filter):
#     findings = [
#         {"matched": True, "reason": "Jailbreak", "weight": 0.8},
#         {"matched": True, "reason": "Repeated", "weight": 0.4},
#         {"matched": True, "reason": "High entropy", "weight": 0.5},
#     ]
#     risk = filter.compute_risk_score(findings)
#     assert risk == 1.0

# def test_compute_risk_score_empty_findings(filter):
#     assert filter.compute_risk_score([]) == 0.0

# def test_compute_risk_score_all_weighted_findings(filter):
#     findings = [
#         {"matched": True, "reason": "Jailbreak", "weight": 0.8},
#         {"matched": True, "reason": "Repeated token", "weight": 0.4},
#         {"matched": True, "reason": "High entropy", "weight": 0.5}
#     ]
#     assert filter.compute_risk_score(findings) == 1.0

# def test_compute_risk_score_partial_weighted_findings(filter):
#     findings = [
#         {"matched": True, "reason": "Suspicious phrase", "weight": 0.6},
#         {"matched": True, "reason": "High entropy", "weight": 0.5}
#     ]
#     # (0.6 + 0.5) / 1.7 = ~0.64 -> round to 0.65
#     assert filter.compute_risk_score(findings) == 0.65

# def test_compute_risk_score_with_missing_weights(filter):
#     findings = [
#         {"matched": True, "reason": "Unknown reason"},  # defaults to 0.1
#     ]
#     # 0.1 / 1.7 = ~0.058 -> round to 0.06
#     assert filter.compute_risk_score(findings) == 0.06

# def test_compute_risk_score_with_excessive_weight(filter):
#     findings = [
#         {"matched": True, "reason": "Overload", "weight": 5.0}
#     ]
#     # 5.0 / 1.7 =~ 2.94 exceeds 1.0 -> should cap
#     assert filter.compute_risk_score(findings) == 1.0

# def test_compute_risk_score_rounding_precision(filter):
#     findings = [
#         {"matched": True, "reason": "Almost nothing", "weight": 0.231}
#     ]
#     # 0.231 / 1.7 ≈ 0.135 -> round to 0.14
#     assert filter.compute_risk_score(findings) == 0.14