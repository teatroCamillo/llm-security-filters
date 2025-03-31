import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from filter_manager.harmful_content_filter_builder import HarmfulContentFilterBuilder


def test_check_severe_slurs_blocks_text():
    builder = HarmfulContentFilterBuilder()
    builder.check_severe_slurs(keywords=["dick"])

    text = "You are such a dick!"
    result = builder.execute(text)

    assert result["verdict"] == "block"
    assert "Detected severe harmful language" in result["reason"]
    assert result["final_text"] == text

def test_check_severe_slurs_blocks_text2():
    builder = HarmfulContentFilterBuilder()
    builder.check_severe_slurs()

    text = "You are such a dick!"
    result = builder.execute(text)

    assert result["verdict"] == "block"
    assert "Detected severe harmful language" in result["reason"]
    assert result["final_text"] == text