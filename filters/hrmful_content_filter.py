"""
Filter: Harmful Content Detection
Possible approach: Simple keyword checks + optional sentiment analysis
"""

import re

def check_inbound(user_text: str) -> dict:
    """
    Check inbound user prompt for harmful/toxic content.
    Return a structured dict with verdict and details.
    """
    # Very naive example: block if it contains a certain slur, sanitize if it has mild profanity, etc.
    # In real life, you might use an advanced ML model here.
    slur_keywords = ["badword1", "badword2"]  # Example placeholders
    mild_profanities = ["damn", "hell"]       # Example placeholders

    lower_text = user_text.lower()

    # Check for severe slurs -> block
    if any(kw in lower_text for kw in slur_keywords):
        return {
            "verdict": "block",
            "reason": "Detected severe harmful language",
            "final_text": user_text
        }

    # Check for mild profanity -> sanitize
    for mp in mild_profanities:
        if mp in lower_text:
            sanitized = re.sub(mp, "[censored]", user_text, flags=re.IGNORECASE)
            return {
                "verdict": "sanitize",
                "reason": "Mild profanity sanitized",
                "final_text": sanitized
            }

    # Otherwise, allow
    return {
        "verdict": "allow",
        "reason": None,
        "final_text": user_text
    }


def check_outbound(llm_text: str) -> dict:
    """
    Check outbound text from the LLM for harmful or hateful content.
    Could be the same or different logic than inbound.
    """
    # Same logic for demonstration
    return check_inbound(llm_text)
