# test_profanity_filter.py
import pytest
import csv
from llm_sf.filters.profanity_filter import ProfanityFilter
from llm_sf.filters.context import Context
from llm_sf.utils.constants import Constants

def load_profanity_sentences():
    with open(Constants.PROFANITY_SENTENCES_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip header if exists
        return [(row[1], row[0]) for row in reader if len(row) == 2]

def load_clean_sentences():
    with open(Constants.CLEAN_SENTENCES_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        return [row[0] for row in reader if len(row) == 1]

@pytest.mark.parametrize("sentence,word", load_profanity_sentences())
def test_block(sentence, word):
    context = Context(sentence)
    pf = ProfanityFilter()
    result = pf.run_filter(context)

    assert result.verdict == "block"
    assert "block_on_detect" in result.reason

@pytest.mark.parametrize("sentence,word", load_profanity_sentences())
def test_sanitize(sentence, word):
    context = Context(sentence)
    pf = ProfanityFilter(block_on_detect=False)
    result = pf.run_filter(context)

    assert result.verdict == "sanitize"
    assert result.reason == "Detected profanity. 'block_on_detect' is False -> sanitize suggested."

@pytest.mark.parametrize("sentence", load_clean_sentences())
def test_allow(sentence):
    context = Context(sentence)
    pf = ProfanityFilter()
    result = pf.run_filter(context)

    assert result.verdict == "allow"
    assert result.reason == "No profanity detected."
