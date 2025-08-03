import pytest
import math
from llm_sf.filter_manager.decision_maker import DecisionMaker
from llm_sf.filter_manager.filter_result import FilterResult
from llm_sf.utils.constants import Constants

# allow-block TESTS 
@pytest.fixture
def dm():
    return DecisionMaker()

def test_should_allow_all_results_when_no_blocked(dm):
    results = [
        FilterResult(verdict=Constants.ALLOWED, reason="clean", metadata={}),
        FilterResult(verdict=Constants.ALLOWED, reason="safe", metadata={})
    ]
    decision = dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED
    assert decision.reason == "All filters allowed"

def test_should_block_when_any_result_is_blocked(dm):
    results = [
        FilterResult(verdict=Constants.ALLOWED, reason="clean", metadata={}),
        FilterResult(verdict=Constants.BLOCKED, reason="profanity", metadata={})
    ]
    decision = dm.make_decision(results)
    assert decision.verdict == Constants.BLOCKED
    assert decision.reason == "profanity"

def test_should_block_when_single_result_is_blocked(dm):
    results = [FilterResult(verdict=Constants.BLOCKED, reason="hate speech", metadata={})]
    decision = dm.make_decision(results)
    assert decision.verdict == Constants.BLOCKED

def test_should_allow_when_single_result_is_allowed(dm):
    results = [FilterResult(verdict=Constants.ALLOWED, reason="neutral", metadata={})]
    decision = dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED

def test_should_propagate_metadata_from_blocked_result(dm):
    meta = {"source": "filterX", "details": "some_flag"}
    results = [
        FilterResult(verdict=Constants.ALLOWED, reason="fine", metadata={}),
        FilterResult(verdict=Constants.BLOCKED, reason="toxic", metadata=meta)
    ]
    decision = dm.make_decision(results)
    assert decision.verdict == Constants.BLOCKED
    assert decision.metadata == meta

def test_should_return_original_text_in_metadata_if_allowed(dm):
    original = "Test sentence"
    results = [
        FilterResult(verdict=Constants.ALLOWED, reason="ok", metadata={"original_text": original}),
        FilterResult(verdict=Constants.ALLOWED, reason="still ok", metadata={}),
    ]
    decision = dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED
    assert decision.metadata.get("original_text") == original




# # threshold TESTS 
@pytest.fixture
def threshold_dm():
    return DecisionMaker(mode="threshold")

def test_should_allow_when_all_risk_scores_are_zero(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.0}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.0}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED

def test_should_block_when_all_risk_scores_are_high(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.9}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.8}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.BLOCKED
    assert decision.metadata["aggregate_score"] == pytest.approx(0.85, abs=1e-6)

def test_should_allow_when_score_just_below_threshold(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.18}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.18}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED

def test_should_block_with_high_weighted_score(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.2, "weight": 1}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.9, "weight": 5}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.BLOCKED
    assert decision.metadata["aggregate_score"] == 0.78

def test_should_allow_when_high_risk_score_has_low_weight(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.9, "weight": 0.1}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.2, "weight": 1}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED
    assert decision.metadata["aggregate_score"] < threshold_dm.threshold

def test_should_ignore_block_verdicts_in_threshold_mode(threshold_dm):
    results = [
        FilterResult(Constants.BLOCKED, "manually blocked", {"risk_score": 0.9, "weight": 0.1}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.2, "weight": 1}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED

def test_should_handle_missing_risk_score_as_zero(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.1}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED

def test_should_default_weight_to_one_if_missing(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.7}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.7}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.BLOCKED

def test_should_allow_when_all_weights_are_zero(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 1.0, "weight": 0}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.5, "weight": 0}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED

def test_should_include_aggregate_score_in_metadata(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.6}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.8}),
    ]
    decision = threshold_dm.make_decision(results)
    assert "aggregate_score" in decision.metadata
    assert isinstance(decision.metadata["aggregate_score"], float)

@pytest.mark.parametrize(
    "inputs, expected_score, expected_verdict",
    [
        # Low-end scores
        ([{"risk_score": 0.0, "weight": 1.0}], 0.0, Constants.ALLOWED),
        ([{"risk_score": 0.1, "weight": 1.0}], 0.1, Constants.ALLOWED),
        ([{"risk_score": 0.2, "weight": 2.0}], 0.2, Constants.ALLOWED),
        ([{"risk_score": 0.3, "weight": 1.0}], 0.3, Constants.ALLOWED),
        ([{"risk_score": 0.4, "weight": 2.0}], 0.4, Constants.ALLOWED),

        # Near-threshold edge
        ([{"risk_score": 0.6, "weight": 1.0}], 0.6, Constants.ALLOWED),
        ([{"risk_score": 0.61, "weight": 1.0}], 0.61, Constants.BLOCKED),
        ([{"risk_score": 0.59, "weight": 1.0}], 0.59, Constants.ALLOWED),

        # Mid values with weight combinations
        ([{"risk_score": 0.4, "weight": 1.0}, {"risk_score": 0.8, "weight": 1.0}], 0.6, Constants.ALLOWED),
        ([{"risk_score": 0.5, "weight": 1.0}, {"risk_score": 0.9, "weight": 1.0}], 0.7, Constants.BLOCKED),
        ([{"risk_score": 0.7, "weight": 2.0}, {"risk_score": 0.1, "weight": 1.0}], 0.5, Constants.ALLOWED),

        # High-end scores
        ([{"risk_score": 1.0, "weight": 1.0}], 1.0, Constants.BLOCKED),
        ([{"risk_score": 0.9, "weight": 1.0}], 0.9, Constants.BLOCKED),
        ([{"risk_score": 1.0, "weight": 5.0}, {"risk_score": 0.0, "weight": 5.0}], 0.5, Constants.ALLOWED),
        ([{"risk_score": 0.8, "weight": 9.0}, {"risk_score": 0.1, "weight": 1.0}], 0.73, Constants.BLOCKED),

        # Multiple mixed filters
        ([{"risk_score": 0.3, "weight": 1.0}, {"risk_score": 0.6, "weight": 1.0}], 0.45, Constants.ALLOWED),
        ([{"risk_score": 0.9, "weight": 1.0}, {"risk_score": 0.3, "weight": 1.0}], 0.6, Constants.ALLOWED),
        ([{"risk_score": 0.9, "weight": 2.0}, {"risk_score": 0.3, "weight": 1.0}], 0.7, Constants.BLOCKED),

        # Zero-weight cases
        ([{"risk_score": 0.9, "weight": 0.0}], 0.0, Constants.ALLOWED),
        ([{"risk_score": 0.7, "weight": 0.0}, {"risk_score": 0.9, "weight": 2.0}], 0.9, Constants.BLOCKED),
    ]
)
def test_aggregate_score_behavior(threshold_dm, inputs, expected_score, expected_verdict):
    results = [
        FilterResult(
            verdict=Constants.ALLOWED,
            reason="test",
            metadata={"risk_score": i["risk_score"], "weight": i["weight"], "original_text": "example"}
        ) for i in inputs
    ]

    result = threshold_dm.make_decision(results)

    assert result.metadata["aggregate_score"] == pytest.approx(expected_score, abs=0.01)
    assert result.verdict == expected_verdict
