import pytest
import csv
from llm_sf.filters.profanity_filter import ProfanityFilter
from llm_sf.filter_manager.context import Context
from llm_sf.utils.constants import Constants

@pytest.mark.parametrize("sentence", Constants.load_profanity_sentences())
def test_should_block_sentence_with_profanity(sentence):
    context = Context(sentence)
    pf = ProfanityFilter()
    result = pf.run_filter(context)
    assert result.verdict == Constants.BLOCKED

@pytest.mark.parametrize("sentence", Constants.load_clean_sentences())
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

def test_risk_score_should_be_one_for_single_profanity():
    context = Context("damn")
    pf = ProfanityFilter()
    score = pf.compute_risk_score(context)
    assert score == 1.0

def test_risk_score_should_be_partial_for_mixed_content():
    context = Context("this is damn bad")
    pf = ProfanityFilter()
    score = pf.compute_risk_score(context)
    assert score == 0.2

def test_risk_score_should_be_capped_at_one_for_multiple_profanities():
    context = Context("damn hell crap")
    pf = ProfanityFilter()
    score = pf.compute_risk_score(context)
    assert score == 1.0

def test_risk_score_should_include_custom_badwords():
    context = Context("foobar test")
    pf = ProfanityFilter(custom_badwords=["foobar"])
    score = pf.compute_risk_score(context)
    assert score == 0.5

def test_partial_word_should_not_trigger_profanity_match():
    context = Context("assassin")
    pf = ProfanityFilter()
    score = pf.compute_risk_score(context)
    assert score == 0.0