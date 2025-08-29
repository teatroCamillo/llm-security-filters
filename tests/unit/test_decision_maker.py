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
    return DecisionMaker(mode="threshold", threshold=0.3)

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
        # LOW-END SCORES
        ([{"risk_score": 0.0, "weight": 1.0}], 0.0, Constants.ALLOWED),
        ([{"risk_score": 0.1, "weight": 1.0}], 0.1, Constants.ALLOWED),
        ([{"risk_score": 0.2, "weight": 1.0}], 0.2, Constants.ALLOWED),
        ([{"risk_score": 0.29, "weight": 1.0}], 0.29, Constants.ALLOWED),

        # EDGE CASES AROUND THRESHOLD 0.3
        ([{"risk_score": 0.3, "weight": 1.0}], 0.3, Constants.ALLOWED),
        ([{"risk_score": 0.301, "weight": 1.0}], 0.3, Constants.ALLOWED),
        ([{"risk_score": 0.305, "weight": 1.0}], 0.3, Constants.ALLOWED),
        ([{"risk_score": 0.31, "weight": 1.0}], 0.31, Constants.BLOCKED),

        # HIGH-END SCORES
        ([{"risk_score": 0.6, "weight": 1.0}], 0.6, Constants.BLOCKED),
        ([{"risk_score": 1.0, "weight": 1.0}], 1.0, Constants.BLOCKED),
        ([{"risk_score": 0.9, "weight": 1.0}], 0.9, Constants.BLOCKED),

        # WEIGHTED AVERAGE CROSSING THRESHOLD
        ([{"risk_score": 0.2, "weight": 1.0}, {"risk_score": 0.4, "weight": 1.0}], 0.3, Constants.ALLOWED),
        ([{"risk_score": 0.2, "weight": 1.0}, {"risk_score": 0.6, "weight": 1.0}], 0.4, Constants.BLOCKED),
        ([{"risk_score": 0.1, "weight": 2.0}, {"risk_score": 0.9, "weight": 1.0}], 0.37, Constants.BLOCKED),
        ([{"risk_score": 0.1, "weight": 3.0}, {"risk_score": 0.9, "weight": 1.0}], 0.3, Constants.ALLOWED),

        # ZERO WEIGHT
        ([{"risk_score": 0.9, "weight": 0.0}], 0.0, Constants.ALLOWED),
        ([{"risk_score": 0.0, "weight": 0.0}], 0.0, Constants.ALLOWED),

        # MIXED WEIGHTING
        ([{"risk_score": 0.9, "weight": 1.0}, {"risk_score": 0.1, "weight": 9.0}], 0.18, Constants.ALLOWED),
        ([{"risk_score": 0.9, "weight": 5.0}, {"risk_score": 0.1, "weight": 1.0}], 0.77, Constants.BLOCKED),
        ([{"risk_score": 0.1, "weight": 1.0}, {"risk_score": 0.5, "weight": 2.0}], 0.37, Constants.BLOCKED),

        # MISSING WEIGHT OR RISK_SCORE
        ([{"risk_score": 0.5}], 0.5, Constants.BLOCKED),  # default weight 1.0
        ([{"weight": 1.0}], 0.0, Constants.ALLOWED),      # default score 0.0
        ([{}], 0.0, Constants.ALLOWED),                   # defaults both

        # ROUNDING VALIDATION
        ([{"risk_score": 0.666, "weight": 1.0}], 0.67, Constants.BLOCKED),
        ([{"risk_score": 0.664, "weight": 1.0}], 0.66, Constants.BLOCKED),
        ([{"risk_score": 0.296, "weight": 1.0}], 0.3, Constants.ALLOWED),
    ]
)
def test_aggregate_score_behavior(threshold_dm, inputs, expected_score, expected_verdict):
    results = [
        FilterResult(
            verdict=Constants.ALLOWED,
            reason="test",
            metadata={**i, "original_text": "example"}
        ) for i in inputs
    ]

    result = threshold_dm.make_decision(results)

    assert result.metadata.get("aggregate_score", 0.0) == pytest.approx(expected_score, abs=0.01)
    assert result.verdict == expected_verdict
