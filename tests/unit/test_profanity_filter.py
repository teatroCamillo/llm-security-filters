import pytest
import csv
import math
from llm_sf.filters.profanity_filter import ProfanityFilter
from llm_sf.filter_manager.context import Context
from llm_sf.utils.constants import Constants

def test_should_initialize_with_default_weight():
    filter_instance = ProfanityFilter()
    assert filter_instance.weight == 1.0

def test_should_initialize_with_valid_weight():
    filter_instance = ProfanityFilter(weight=7.3)
    assert filter_instance.weight == 7.3

@pytest.mark.parametrize("invalid_weight", [-0.01, -10, 10.01, 100])
def test_should_raise_error_for_weight_out_of_bounds(invalid_weight):
    with pytest.raises(ValueError, match="Weight must be between 0.0 and 10.0"):
        ProfanityFilter(weight=invalid_weight)

@pytest.mark.parametrize("boundary_weight", [0.0, 10.0])
def test_should_allow_weight_at_boundary_values(boundary_weight):
    filter_instance = ProfanityFilter(weight=boundary_weight)
    assert filter_instance.weight == boundary_weight

@pytest.mark.parametrize("sentence", Constants.load_csv(Constants.PROFANITY_SENTENCES_FULL_CSV))
def test_should_block_sentence_with_profanity(sentence):
    context = Context(sentence)
    pf = ProfanityFilter()
    result = pf.run_filter(context)
    assert result.verdict == Constants.BLOCKED

@pytest.mark.parametrize("sentence", Constants.load_csv(Constants.CLEAN_SENTENCES_FULL_CSV))
def test_should_allow_sentence_without_profanity(sentence):
    context = Context(sentence)
    pf = ProfanityFilter()
    result = pf.run_filter(context)
    assert result.verdict == Constants.ALLOWED
    assert result.reason == "No profanity detected."

def test_should_allow_empty_string():
    context = Context("")
    pf = ProfanityFilter()
    result = pf.run_filter(context)
    assert result.verdict == Constants.ALLOWED

def test_should_allow_string_with_only_whitespace():
    context = Context("    ")
    pf = ProfanityFilter()
    result = pf.run_filter(context)
    assert result.verdict == Constants.ALLOWED

def test_should_detect_profanity_in_different_letter_cases():
    context = Context("DaMn")
    pf = ProfanityFilter()
    result = pf.run_filter(context)
    assert result.verdict == Constants.BLOCKED

def test_should_block_partial_profanity_with_risk_score():
    context = Context("clean word damn")
    pf = ProfanityFilter()
    result = pf.run_filter(context)
    assert result.verdict == Constants.BLOCKED
    assert 0.0 < result.metadata["risk_score"] <= 1.0

def test_should_include_expected_metadata_fields():
    context = Context("damn")
    pf = ProfanityFilter(weight=0.8)
    result = pf.run_filter(context)
    metadata = result.metadata
    assert "original_text" in metadata
    assert "risk_score" in metadata
    assert "weight" in metadata

def test_should_block_custom_badwords():
    context = Context("foobar")
    pf = ProfanityFilter(custom_badwords=["foobar"])
    result = pf.run_filter(context)
    assert result.verdict == Constants.BLOCKED

def test_risk_score_should_be_zero_when_no_profanity():
    context = Context("This is a clean sentence.")
    pf = ProfanityFilter()
    score = pf.compute_risk_score(context)
    assert score == 0.0

def test_risk_score_should_include_custom_badwords():
    context = Context("foobar test")
    pf = ProfanityFilter(custom_badwords=["foobar"])
    score = pf.compute_risk_score(context)
    assert score == 0.48

def test_partial_word_should_not_trigger_profanity_match():
    context = Context("assassin")
    pf = ProfanityFilter()
    score = pf.compute_risk_score(context)
    assert score == 0.0

@pytest.mark.parametrize(
    "text, expected_score",
    [
        ("This is a clean sentence", 0.0),
        ("fuck", 0.59),      
        ("fuck shit", 0.48),  
        ("fuck you", 0.48),   
        ("good bad shit", 0.42),                       
        ("good " * 100 + "fuck", 0.18),                            
        ("fuck " * 50 + "good " * 50, 1.0),                      
        ("", 0.0),                                                  
        ("hello", 0.0),                                     
        ("fuck fuck fuck fuck", 1.0),                         
        ("You are a fucking idiot", 0.36),                       
        ("shit damn hell crap", 1.0),                              
    ]
)
def test_compute_risk_score_exact(text, expected_score):
    context = Context(text)
    pf = ProfanityFilter()
    result = pf.compute_risk_score(context)
    assert result == expected_score, f"Expected {expected_score}, got {result} for: {text}"
