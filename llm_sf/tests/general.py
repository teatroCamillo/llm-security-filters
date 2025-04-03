import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from filters.context import Context
from filters.profanity_filter import ProfanityFilter

def test_check_severe_slurs_blocks_text():
    """
    Test sprawdza, czy wykrycie słowa wulgarnego powoduje block
    przy 'block_on_detect=True'.
    """
    context = Context("This is a damn code!")
    pf = ProfanityFilter(
        custom_badwords=["damn", "shit"],
        use_default_wordlist=False,
        block_on_detect=True
    )
    result = pf.run_filter(context)
    assert result.verdict == "block"
    assert "Detected profanity" in result.reason
    
@pytest.mark.parametrize("input_text, expected_verdict", [
    ("This is damn", "block"),
    ("Damn, that's hell", "block"),
    ("Everything is crap", "block"),
])
def test_check_text(input_text, expected_verdict):
    """
    Test parametryzowany – sprawdzamy różne teksty i czy filtr je blokuje (lub przepuszcza).
    """
    context = Context(input_text)
    pf = ProfanityFilter(
        block_on_detect=True
    )
    result = pf.run_filter(context)
    assert result.verdict == expected_verdict, (
        f"Dla tekstu '{input_text}' oczekiwano werdyktu '{expected_verdict}', "
        f"ale otrzymano '{result.verdict}'."
    )