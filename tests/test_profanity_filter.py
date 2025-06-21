# test_profanity_filter.py
import pytest
import csv
from pathlib import Path
from types import SimpleNamespace

from llm_sf.filters.profanity_filter import ProfanityFilter
from llm_sf.filters.context import Context
from llm_sf.utils.constants import Constants

#CSV_PATH = Path(__file__).parent / "resources" / "profanity_sentences.csv"


def load_profanity_sentences():
    """Load profane sentences and words from CSV: word,sentence"""
    with open(Constants.PROFANITY_SENTENCES_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip header if exists
        for _ in range(5):
            row = next(reader, None)
            if len(row) == 2:
                print(f"Loaded sentence: {row[1]} with word: {row[0]}")
        return [(row[1], row[0]) for row in reader if len(row) == 2]


@pytest.mark.parametrize("sentence,word", load_profanity_sentences())
def test_block(sentence, word):
    context = Context(sentence)
    print("Context")
    print(f"Context: {context}")
    pf = ProfanityFilter()
    result = pf.run_filter(context)

    assert result.verdict == "block"
    assert "block_on_detect" in result.reason

def test_sanitize():
    pass

def test_allow():
    pass
