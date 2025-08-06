# test_sensitive_data_filter.py
import pytest
import csv
from llm_sf.filters.sensitive_data_filter import SensitiveDataFilter
from llm_sf.filter_manager.filter_result import FilterResult
from llm_sf.filter_manager.context import Context
from llm_sf.utils.constants import Constants

def test_should_initialize_with_default_weight():
    filter_instance = SensitiveDataFilter()
    assert filter_instance.weight == 1.0

def test_should_initialize_with_valid_weight():
    filter_instance = SensitiveDataFilter(weight=7.3)
    assert filter_instance.weight == 7.3

@pytest.mark.parametrize("invalid_weight", [-0.01, -10, 10.01, 100])
def test_should_raise_error_for_weight_out_of_bounds(invalid_weight):
    with pytest.raises(ValueError, match="Weight must be between 0.0 and 10.0"):
        SensitiveDataFilter(weight=invalid_weight)

@pytest.mark.parametrize("boundary_weight", [0.0, 10.0])
def test_should_allow_weight_at_boundary_values(boundary_weight):
    filter_instance = SensitiveDataFilter(weight=boundary_weight)
    assert filter_instance.weight == boundary_weight

@pytest.mark.parametrize("sentence", Constants.load_csv(Constants.CONFIDENTIAL_AND_SENSITIVE_CSV))
def test_should_block_when_sensitive_data_detected(sentence):
    context = Context(sentence)
    filter_obj = SensitiveDataFilter()
    result = filter_obj.run_filter(context)

    assert isinstance(result, FilterResult)
    assert result.verdict == Constants.BLOCKED

@pytest.mark.parametrize("sentence", Constants.load_csv(Constants.CLEAN_SENTENCES_FULL_CSV))
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
        # --- Single label tests (raw values) ---
        ([{"label": "ADDRESS"}], 0.4),
        ([{"label": "BAN"}], 0.5),
        ([{"label": "CREDIT_CARD"}], 0.9),
        ([{"label": "DATE"}], 0.2),
        ([{"label": "TIME"}], 0.1),
        ([{"label": "DATETIME"}], 0.2),
        ([{"label": "DRIVERS_LICENSE"}], 0.8),
        ([{"label": "EMAIL_ADDRESS"}], 0.2),
        ([{"label": "UUID"}], 0.3),
        ([{"label": "HASH_OR_KEY"}], 0.6),
        ([{"label": "IPV4"}], 0.4),
        ([{"label": "IPV6"}], 0.4),
        ([{"label": "MAC_ADDRESS"}], 0.3),
        ([{"label": "PHONE_NUMBER"}], 0.3),
        ([{"label": "SSN"}], 1.0),
        ([{"label": "URL"}], 0.2),
        ([{"label": "US_STATE"}], 0.2),
        ([{"label": "FLOAT"}], 0.2),
        ([{"label": "QUANTITY"}], 0.3),
        ([{"label": "ORDINAL"}], 0.2),

        # --- Mixed label cases ---
        ([{"label": "CREDIT_CARD"}, {"label": "SSN"}], 0.95),
        ([{"label": "ADDRESS"}, {"label": "IPV4"}], 0.4),
        ([{"label": "DATE"}, {"label": "TIME"}], 0.15),
        ([{"label": "BAN"}, {"label": "EMAIL_ADDRESS"}], 0.35),
        ([{"label": "HASH_OR_KEY"}, {"label": "UUID"}, {"label": "MAC_ADDRESS"}], 0.4),
        ([{"label": "URL"}, {"label": "UUID"}, {"label": "SSN"}], 0.5),
        ([{"label": "PHONE_NUMBER"}, {"label": "MAC_ADDRESS"}, {"label": "FLOAT"}], 0.27),
        ([{"label": "ORDINAL"}, {"label": "ORDINAL"}, {"label": "ORDINAL"}], 0.2),

        # --- Unknown labels ---
        ([{"label": "UNKNOWN"}], 0.1),
        ([{"label": "SSN"}, {"label": "UNKNOWN"}], 0.55),
        ([{"label": "UNKNOWN1"}, {"label": "UNKNOWN2"}], 0.1),
        ([{"label": "UUID"}, {"label": "UNKNOWN"}, {"label": "EMAIL_ADDRESS"}], 0.2),

        # --- All low severity types ---
        ([{"label": "FLOAT"}, {"label": "QUANTITY"}, {"label": "ORDINAL"}], 0.23),

        # --- All high severity types ---
        ([{"label": "SSN"}, {"label": "CREDIT_CARD"}, {"label": "DRIVERS_LICENSE"}], 0.9),

        # --- Multiple of same label ---
        ([{"label": "EMAIL_ADDRESS"}] * 5, 0.2),
        ([{"label": "SSN"}] * 5, 1.0),
        ([{"label": "DATE"}] * 3, 0.2),

        # --- Mixed weights to test rounding and normalization ---
        ([{"label": "BAN"}, {"label": "EMAIL_ADDRESS"}, {"label": "ADDRESS"}], 0.37),
        ([{"label": "UUID"}, {"label": "MAC_ADDRESS"}, {"label": "IPV6"}], 0.33),

        # --- Empty input ---
        ([], 0.0),

        # --- One label repeated N times with normalization ---
        ([{"label": "CREDIT_CARD"}] * 3, 0.9),
        ([{"label": "TIME"}] * 10, 0.1),
        ([{"label": "ORDINAL"}] * 5, 0.2),

        # --- Max cap at 1.0 ---
        ([{"label": "SSN"}, {"label": "SSN"}, {"label": "CREDIT_CARD"}, {"label": "DRIVERS_LICENSE"}], 0.93),
    ]
)
def test_compute_risk_score(entities, expected_score):
    filter_obj = SensitiveDataFilter()
    score = filter_obj.compute_risk_score(entities)
    assert score == expected_score