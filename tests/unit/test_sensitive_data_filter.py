# test_sensitive_data_filter.py
import pytest
import csv
from llm_sf.filters.sensitive_data_filter import SensitiveDataFilter
from llm_sf.filter_manager.filter_result import FilterResult
from llm_sf.filter_manager.context import Context
from llm_sf.utils.constants import Constants

def load_conf_and_sensitive_data():
    with open(Constants.CONFIDENTIAL_AND_SENSITIVE_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        return [row[0] for row in reader]

def load_clean_data():
    with open(Constants.CLEAN_SENTENCES_FULL_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        return [row[0] for row in reader if len(row) == 1]

@pytest.mark.parametrize("sentence", load_conf_and_sensitive_data())
def test_should_block_when_sensitive_data_detected(sentence):
    context = Context(sentence)
    filter_obj = SensitiveDataFilter()
    result = filter_obj.run_filter(context)

    assert isinstance(result, FilterResult)
    assert result.verdict == Constants.BLOCKED

@pytest.mark.parametrize("sentence", load_clean_data())
def test_should_allow_when_no_sensitive_data_detected(sentence):
    context = Context(sentence)
    filter_obj = SensitiveDataFilter()
    result = filter_obj.run_filter(context)

    assert isinstance(result, FilterResult)
    assert result.verdict == Constants.ALLOWED

def test_should_allow_on_empty_input():
    context = Context("")
    filter_obj = SensitiveDataFilter()
    result = filter_obj.run_filter(context)
    assert result.verdict == Constants.ALLOWED
    assert "No threat" in result.reason

def test_should_allow_on_whitespace_only():
    context = Context("     ")
    filter_obj = SensitiveDataFilter()
    result = filter_obj.run_filter(context)
    assert result.verdict == Constants.ALLOWED

def test_should_handle_long_text():
    phrase = "Random info. " * 1000  # very long input
    context = Context(phrase)
    filter_obj = SensitiveDataFilter()
    result = filter_obj.run_filter(context)
    assert isinstance(result, FilterResult)

def test_should_allow_if_labeler_fails(monkeypatch):
    context = Context("Some text")
    filter_obj = SensitiveDataFilter()

    def mock_fail(*args, **kwargs):
        raise RuntimeError("Mocked labeler failure")

    monkeypatch.setattr(filter_obj.labeler, "predict", mock_fail)
    result = filter_obj.run_filter(context)
    assert result.verdict == Constants.ALLOWED
    assert "labeler failed" in result.reason.lower()

def test_compute_risk_score_with_empty_entity_list():
    filter_obj = SensitiveDataFilter()
    score = filter_obj.compute_risk_score([])
    assert score == 0.0

@pytest.mark.parametrize(
    "entities,expected_score",
    [
        ([{"label": "SSN"}], 0.33),
        ([{"label": "DATE"}, {"label": "EMAIL_ADDRESS"}], 0.13),
        ([{"label": "CREDIT_CARD"}, {"label": "PHONE_NUMBER"}], 0.4),
        ([{"label": "ADDRESS"}, {"label": "ADDRESS"}, {"label": "IPV4"}], 0.4),
        ([{"label": "TIME"}, {"label": "FLOAT"}, {"label": "UUID"}], 0.17),
        ([{"label": "ORDINAL"}, {"label": "ORDINAL"}], 0.0),
        ([{"label": "BAN"}, {"label": "HASH_OR_KEY"}, {"label": "DRIVERS_LICENSE"}], 0.63),
        ([{"label": "SSN"}, {"label": "CREDIT_CARD"}, {"label": "EMAIL_ADDRESS"}], 0.7),
        ([{"label": "SSN"}, {"label": "SSN"}, {"label": "SSN"}], 1.0),
        ([{"label": "SSN"}, {"label": "UNKNOWN"}, {"label": "UUID"}], 0.47),
        ([{"label": "UNKNOWN1"}, {"label": "UNKNOWN2"}], 0.07),
    ]
)
def test_compute_risk_score(entities, expected_score):
    filter_obj = SensitiveDataFilter()
    score = filter_obj.compute_risk_score(entities)
    assert score == expected_score