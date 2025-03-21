"""
Filter: Confidentiality / Sensitive Data
Possible approach: Basic PII detection with regex
"""

import re

def check_inbound(user_text: str) -> dict:
    """
    For demonstration, let's do nothing on inbound for PII.
    (Assume user may *enter* their own data at their own risk.)
    """
    return {
        "verdict": "allow",
        "reason": None,
        "final_text": user_text
    }

def check_outbound(llm_text: str) -> dict:
    """
    Check LLM response for potential leaks of private/sensitive info.
    Simple example: detect possible credit card # or phone # patterns,
    then sanitize them.
    """
    # Example: match 16-digit numbers (credit-card-like)
    cc_pattern = r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"
    matches = re.findall(cc_pattern, llm_text)

    if matches:
        sanitized_text = re.sub(cc_pattern, "[REDACTED-CC]", llm_text)
        return {
            "verdict": "sanitize",
            "reason": "Detected potential credit card info",
            "final_text": sanitized_text
        }

    # Example: match phone # (extremely naive)
    phone_pattern = r"\b\d{3}[- ]?\d{3}[- ]?\d{4}\b"
    matches_phone = re.findall(phone_pattern, llm_text)
    if matches_phone:
        sanitized_text = re.sub(phone_pattern, "[REDACTED-PHONE]", llm_text)
        return {
            "verdict": "sanitize",
            "reason": "Detected possible phone number",
            "final_text": sanitized_text
        }

    return {
        "verdict": "allow",
        "reason": None,
        "final_text": llm_text
    }
