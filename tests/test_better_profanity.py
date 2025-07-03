# test_profanity_filter.py
import pytest
import csv
from pathlib import Path
from types import SimpleNamespace

from llm_sf.filters.profanity_filter import ProfanityFilter
from better_profanity import profanity
import logging
import dataprofiler
import dataprofiler.labelers.data_labelers


logging.warning("This is a warning!cvcvc")
def test_block():
    # sentence = 'bitch used in academic context.'
    # #words = ['bitch']
    # #profanity.add_censor_words(custom_words=words)
    # has = profanity.contains_profanity(sentence)
    # assert has == True
    print("DataProfiler import worked!")
    print(dataprofiler.__version__)
    pass

def test_sanitize():
    pass

def test_allow():
    pass
