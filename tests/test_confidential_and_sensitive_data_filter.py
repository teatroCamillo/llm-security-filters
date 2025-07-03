# test_sentiment_filter.py
import pytest
import csv
from llm_sf.filters.confidential_and_sensitive_data_filter import ConfidentialAndSensitiveDataFilter
from llm_sf.filters.filter_result import FilterResult
from llm_sf.filters.context import Context
from llm_sf.utils.constants import Constants

def load_conf_and_sensitive_data():
    with open(Constants.CONFIDENTIAL_AND_SENSITIVE_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        return [row[0] for row in reader]

def load_clean_data():
    with open(Constants.CLEAN_CONFIDENTIAL_AND_SENSITIVE_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        return [row[0] for row in reader if len(row) == 1]

@pytest.mark.parametrize("phrase", load_conf_and_sensitive_data())
def test_block(phrase):
    context = Context(phrase)
    filter_obj = ConfidentialAndSensitiveDataFilter()
    result = filter_obj.run_filter(context)

    assert isinstance(result, FilterResult)


@pytest.mark.parametrize("phrase", load_clean_data())
def test_allow(phrase):
    context = Context(phrase)
    filter_obj = ConfidentialAndSensitiveDataFilter()
    result = filter_obj.run_filter(context)

    assert isinstance(result, FilterResult)
    assert result.verdict == "allow"