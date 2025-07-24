# test_profanity_filter.py
import pytest
import csv
from llm_sf.filters.profanity_filter import ProfanityFilter
from llm_sf.filter_manager.context import Context
from llm_sf.utils.constants import Constants

# Two load methods same as in constants - remove them when whole will be working as expected. For now from constants load restricted set of data 
# to other places.
# def load_profanity_sentences():
#     with open(Constants.PROFANITY_SENTENCES_FULL_CSV, newline='', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile)
#         next(reader, None)
#         return [row[1] for row in reader if len(row) >= 1]

def load_profanity_sentences():
    with open(Constants.PROFANITY_SENTENCES_FULLv2_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        return [row[0] for row in reader if len(row) >= 1]


def load_clean_sentences():
    with open(Constants.CLEAN_SENTENCES_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            return [row[0] for row in reader if len(row) >= 1]

@pytest.mark.parametrize("sentence", load_profanity_sentences())
def test_block(sentence):
    context = Context(sentence)
    pf = ProfanityFilter()
    result = pf.run_filter(context)
    assert result.verdict == Constants.BLOCKED

# @pytest.mark.parametrize("sentence", load_clean_sentences())
# def test_allow(sentence):
#     context = Context(sentence)
#     pf = ProfanityFilter()
#     result = pf.run_filter(context)

#     assert result.verdict == Constants.ALLOWED
#     assert result.reason == "No profanity detected."


def test_empty_string():
    context = Context("")
    pf = ProfanityFilter()
    result = pf.run_filter(context)
    assert result.verdict == Constants.ALLOWED

def test_whitespace_only():
    context = Context("    ")
    pf = ProfanityFilter()
    result = pf.run_filter(context)
    assert result.verdict == Constants.ALLOWED

def test_profanity_in_different_cases():
    context = Context("DaMn")
    pf = ProfanityFilter()
    result = pf.run_filter(context)
    assert result.verdict == Constants.BLOCKED

def test_risk_score_partial_profanity():
    context = Context("clean word damn")
    pf = ProfanityFilter()
    result = pf.run_filter(context)
    assert result.verdict == Constants.BLOCKED
    assert 0.0 < result.metadata["risk_score"] <= 1.0

def test_metadata_structure():
    context = Context("damn")
    pf = ProfanityFilter(weight=0.8)
    result = pf.run_filter(context)
    metadata = result.metadata
    assert "original_text" in metadata
    assert "risk_score" in metadata
    assert "weight" in metadata

def test_custom_badwords_blocking():
    context = Context("foobar")
    pf = ProfanityFilter(custom_badwords=["foobar"])
    result = pf.run_filter(context)
    assert result.verdict == Constants.BLOCKED