# test_word_mutator.py
import pytest
import csv
from llm_sf.filters.sentiment_filter import SentimentFilter
from llm_sf.filters.context import Context
from llm_sf.utils.constants import Constants
from llm_sf.utils.word_mutator import WordMutator


def test_no1():
    mutator = WordMutator()
    mutator.generate_mutations("fuck")
    for variant in mutator.get_mutations("fuck"):
        print(variant)
    assert len(mutator.get_mutations("fuck")) == 1
