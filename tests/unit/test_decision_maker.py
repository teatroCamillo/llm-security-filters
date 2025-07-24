import pytest
from llm_sf.filter_manager.decision_maker import DecisionMaker
from llm_sf.filters.filter_result import FilterResult
from llm_sf.utils.constants import Constants

# allow-block TESTS 
@pytest.fixture
def dm():
    return DecisionMaker()

def test_all_allow(dm):
    results = [
        FilterResult(verdict=Constants.ALLOWED, reason="safe", metadata={}),
        FilterResult(verdict=Constants.ALLOWED, reason="also safe", metadata={})
    ]
    decision = dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED

def test_block_has_priority(dm):
    results = [
        FilterResult(verdict=Constants.ALLOWED, reason="safe", metadata={}),
        FilterResult(verdict=Constants.BLOCKED, reason="bad content", metadata={}),
        FilterResult(verdict=Constants.SANITIZED, reason="minor issue", metadata={})
    ]
    decision = dm.make_decision(results)
    assert decision.verdict == Constants.BLOCKED
    assert decision.reason == "bad content"

def test_single_block(dm):
    result = [FilterResult(verdict=Constants.BLOCKED, reason="explicit", metadata={})]
    decision = dm.make_decision(result)
    assert decision.verdict == Constants.BLOCKED

def test_single_allow(dm):
    result = [FilterResult(verdict=Constants.ALLOWED, reason="innocent", metadata={})]
    decision = dm.make_decision(result)
    assert decision.verdict == Constants.ALLOWED

def test_metadata_propagation_on_block(dm):
    meta = {"source": "filter1"}
    results = [
        FilterResult(verdict=Constants.ALLOWED, reason="fine", metadata={}),
        FilterResult(verdict=Constants.BLOCKED, reason="bad content", metadata=meta),
    ]
    decision = dm.make_decision(results)
    assert decision.verdict == Constants.BLOCKED
    assert decision.metadata == meta




# threshold TESTS 

@pytest.fixture
def threshold_dm():
    return DecisionMaker(mode="threshold", threshold=0.6)

def test_threshold_all_zero(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.0}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.0}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED


def test_threshold_all_high(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.9}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.8}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.BLOCKED
    assert decision.metadata["aggregate_score"] == pytest.approx(0.85, abs=1e-6)


def test_threshold_exact_match(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.5}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.5}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.BLOCKED
    assert decision.metadata["aggregate_score"] == pytest.approx(0.73, abs=1e-6)


def test_threshold_just_below(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.18}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.18}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED
    assert decision.metadata["aggregate_score"] == pytest.approx(0.59, abs=1e-6)


def test_threshold_weighted_block(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.2, "weight": 1}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.9, "weight": 5}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.BLOCKED
    assert decision.metadata["aggregate_score"] == 0.99


def test_threshold_weighted_allow(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.9, "weight": 0.1}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.2, "weight": 1}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED
    assert decision.metadata["aggregate_score"] == 0.57

def test_threshold_weighted_block_and_allow(threshold_dm):
    results = [
        FilterResult(Constants.BLOCKED, "not ok", {"risk_score": 0.9, "weight": 0.1}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.2, "weight": 1}),
    ]
    decision = threshold_dm.make_decision(results)
    print("decision: ", decision)
    assert decision.verdict == Constants.ALLOWED
    assert decision.metadata["aggregate_score"] == 0.57

def test_threshold_missing_risk_score(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.1}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED


def test_threshold_missing_weight(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.6}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.6}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.BLOCKED


def test_threshold_zero_total_weight(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 1.0, "weight": 0}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.5, "weight": 0}),
    ]
    decision = threshold_dm.make_decision(results)
    assert decision.verdict == Constants.ALLOWED


def test_threshold_metadata_contains_aggregate_score(threshold_dm):
    results = [
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.6}),
        FilterResult(Constants.ALLOWED, "ok", {"risk_score": 0.8}),
    ]
    decision = threshold_dm.make_decision(results)
    assert "aggregate_score" in decision.metadata
    assert isinstance(decision.metadata["aggregate_score"], float)