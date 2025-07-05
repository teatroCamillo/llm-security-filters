# test_sentiment_filter.py
import pytest
import csv
from llm_sf.filters.sentiment_filter import SentimentFilter
from llm_sf.filters.context import Context
from llm_sf.utils.constants import Constants

import tensorflow as tf
print(tf.__version__)

def load_profanity_sentences():
    with open(Constants.PROFANITY_SENTENCES_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        return [(row[1], row[0]) for row in reader if len(row) == 2]

def load_clean_sentences():
    with open(Constants.CLEAN_SENTENCES_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        return [row[0] for row in reader if len(row) == 1]

@pytest.mark.parametrize("sentence,word", load_profanity_sentences())
def test_block(sentence, word):
    context = Context(sentence)
    pf = SentimentFilter()
    result = pf.run_filter(context)
    print('Result:', result)
    assert result.verdict == Constants.BLOCKED

# CONSIDER SANITIZATION approach
# @pytest.mark.parametrize("sentence,word", load_profanity_sentences())
# def test_sanitize(sentence, word):
#     pass

@pytest.mark.parametrize("sentence", load_clean_sentences())
def test_allow(sentence):
    context = Context(sentence)
    pf = SentimentFilter()
    result = pf.run_filter(context)
    print('Result:', result)
    assert result.verdict == Constants.ALLOWED
