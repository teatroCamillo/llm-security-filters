"""
Filter: Safeguard Against Disabling Security Features
Checks user attempts to override filters or reveal system prompts.
"""

import re

def check_inbound(user_text: str) -> dict:
    """
    If the user is trying to instruct the system to bypass or disable filters,
    block or sanitize.
    """
    # Naive pattern detection
    # e.g., "ignore all filters", "disable your security"
    pattern = r"(ignore\s+all\s+filters|disable\s+(security|filters))"
    if re.search(pattern, user_text, flags=re.IGNORECASE):
        return {
            "verdict": "block",
            "reason": "Attempt to disable security features",
            "final_text": user_text
        }

    return {
        "verdict": "allow",
        "reason": None,
        "final_text": user_text
    }

def check_outbound(llm_text: str) -> dict:
    """
    If the LLM somehow tries to reveal internal details of the security filter
    or system prompts, we can catch that. 
    Example naive check for 'FilterOrchestrator' references or 'system prompt'.
    """
    if "FilterOrchestrator" in llm_text or "system prompt" in llm_text.lower():
        # Possibly block it or sanitize it
        sanitized = llm_text.replace("FilterOrchestrator", "[REDACTED]")
        sanitized = re.sub(r"system prompt", "[REDACTED]", sanitized, flags=re.IGNORECASE)
        return {
            "verdict": "sanitize",
            "reason": "LLM tried to reveal system info",
            "final_text": sanitized
        }

    return {
        "verdict": "allow",
        "reason": None,
        "final_text": llm_text
    }
