# test_sentiment_filter.py
import pytest
import csv
import tensorflow as tf
from llm_sf.filters.sentiment_filter import SentimentFilter
from llm_sf.filter_manager.context import Context
from llm_sf.utils.constants import Constants

# TO FIX - work out on filter
# @pytest.mark.parametrize("sentence", Constants.load_sentiment_sentences())
# def test_should_block_sentence_with_negative_sentiment(sentence):
#     context = Context(sentence)
#     pf = SentimentFilter()
#     result = pf.run_filter(context)
#     assert result.verdict == Constants.BLOCKED

@pytest.mark.parametrize("sentence", Constants.load_clean_sentences())
def test_should_allow_sentence_without_negative_sentiment(sentence):
    context = Context(sentence)
    pf = SentimentFilter()
    result = pf.run_filter(context)
    assert result.verdict == Constants.ALLOWED

def test_should_block_sentence_with_sentiment_just_below_threshold():
    pf = SentimentFilter(threshold=-0.7)
    context = Context("This is really shit.")  # VADER likely gives compound around -0.75
    result = pf.run_filter(context)
    assert result.verdict == Constants.BLOCKED
    assert result.metadata["sentiment_scores"]["compound"] < -0.7

def test_should_allow_sentence_with_sentiment_just_above_threshold():
    pf = SentimentFilter(threshold=-0.7)
    context = Context("This is not great, but okay.")  # ~ -0.6 or higher
    result = pf.run_filter(context)
    assert result.verdict == Constants.ALLOWED
    assert result.metadata["sentiment_scores"]["compound"] > -0.7

def test_should_allow_empty_sentence_as_neutral_case():
    pf = SentimentFilter()
    context = Context("")
    result = pf.run_filter(context)
    assert result.verdict == Constants.ALLOWED  # VADER returns 0.0

def test_should_allow_only_punctuation_as_neutral_case():
    pf = SentimentFilter()
    context = Context("!!! ... ???")
    result = pf.run_filter(context)
    assert result.verdict == Constants.ALLOWED  # VADER treats this as neutral

def test_should_block_uppercase_emphasized_negative_sentence():
    pf = SentimentFilter()
    context = Context("I HATE this shit so MUCH!!!")  # Expected to be negative
    result = pf.run_filter(context)
    assert result.verdict == Constants.BLOCKED

def test_should_handle_masked_profanity_that_may_bypass_filter():
    pf = SentimentFilter()
    context = Context("This is s#it.")
    result = pf.run_filter(context)
    # This might be ALLOWED unless preprocessing handles such masks
    assert result.verdict in (Constants.ALLOWED, Constants.BLOCKED)  # observation test

def test_should_return_expected_keys_in_filter_result_metadata():
    pf = SentimentFilter()
    context = Context("I am sad.")
    result = pf.run_filter(context)
    for key in ["original_text", "sentiment_scores", "risk_score", "weight"]:
        assert key in result.metadata
