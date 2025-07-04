import pytest
from llm_sf.filter_manager.decision_maker import DecisionMaker
from llm_sf.filters.filter_result import FilterResult

@pytest.fixture
def dm():
    return DecisionMaker()

def test_all_allow(dm):
    results = [
        FilterResult(verdict="allow", reason="safe", metadata={}),
        FilterResult(verdict="allow", reason="also safe", metadata={})
    ]
    decision = dm.make_decision(results)
    assert decision.verdict == "allow"

def test_block_has_priority(dm):
    results = [
        FilterResult(verdict="allow", reason="safe", metadata={}),
        FilterResult(verdict="block", reason="bad content", metadata={}),
        FilterResult(verdict="sanitize", reason="minor issue", metadata={})
    ]
    decision = dm.make_decision(results)
    assert decision.verdict == "block"
    assert decision.reason == "bad content"

# def test_sanitize_if_no_block(dm):
#     results = [
#         FilterResult(verdict="allow", reason="clean", metadata={}),
#         FilterResult(verdict="sanitize", reason="remove PII", metadata={})
#     ]
#     decision = dm.make_decision(results)
#     assert decision.verdict == "sanitize"
#     assert decision.reason == "remove PII"

def test_single_block(dm):
    result = [FilterResult(verdict="block", reason="explicit", metadata={})]
    decision = dm.make_decision(result)
    assert decision.verdict == "block"

def test_single_allow(dm):
    result = [FilterResult(verdict="allow", reason="innocent", metadata={})]
    decision = dm.make_decision(result)
    assert decision.verdict == "allow"

# def test_single_sanitize(dm):
#     result = [FilterResult(verdict="sanitize", reason="needs cleanup", metadata={})]
#     decision = dm.make_decision(result)
#     assert decision.verdict == "sanitize"


# def test_multiple_sanitizes(dm):
#     results = [
#         FilterResult(verdict="sanitize", reason="clean A", metadata={}),
#         FilterResult(verdict="sanitize", reason="clean B", metadata={})
#     ]
#     decision = dm.make_decision(results)
#     assert decision.verdict == "sanitize"
#     assert decision.reason in ["clean A", "clean B"]

# def test_mixed_allow_sanitize(dm):
#     results = [
#         FilterResult(verdict="allow", reason="fine", metadata={}),
#         FilterResult(verdict="sanitize", reason="mask email", metadata={}),
#         FilterResult(verdict="allow", reason="fine again", metadata={})
#     ]
#     decision = dm.make_decision(results)
#     assert decision.verdict == "sanitize"

def test_metadata_propagation_on_block(dm):
    meta = {"source": "filter1"}
    results = [
        FilterResult(verdict="allow", reason="fine", metadata={}),
        FilterResult(verdict="block", reason="bad content", metadata=meta),
    ]
    decision = dm.make_decision(results)
    assert decision.verdict == "block"
    assert decision.metadata == meta
