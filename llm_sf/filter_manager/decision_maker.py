"""
decision_maker.py
Utility to merge the results of multiple filters in parallel mode.

DM powinnien być brdziej elestyczny niż sekwencyjne podejście gdyż za pomocą argumentów
można łatwiej sterować progiem a co za tym idzie dostosować do oczekiwań użytkownika.

"""

def combine_parallel_results(results):
    """
    'results' is a list of dictionaries like:
    [ {"verdict": "allow", "final_text": "...", ...}, {"verdict": "block", ...}, ... ]
    
    This function decides what to do overall.
    E.g. if any filter says "block", block everything.
         if any filter says "sanitize", unify sanitized outputs (some logic).
         else allow.
    """
    # If any says block, we block
    for r in results:
        if r["verdict"] == "block":
            return {
                "verdict": "block",
                "reason": r.get("reason", "No reason"),
                "final_text": r.get("final_text", "")
            }

    # If none blocked, but some have "sanitize", pick a sanitized union
    # (In a real scenario, you may need more sophisticated logic to unify sanitized texts.)
    final_text = None
    reason = []
    sanitized = False
    for r in results:
        if r["verdict"] == "sanitize":
            sanitized = True
            reason.append(r["reason"])
            # Over-simplification: just take the first sanitized text
            if final_text is None:
                final_text = r["final_text"]
        else:
            # If r is "allow" and no final_text picked yet, we keep it as candidate
            if final_text is None:
                final_text = r["final_text"]

    if sanitized:
        return {
            "verdict": "sanitize",
            "reason": "; ".join(reason),
            "final_text": final_text
        }

    # Otherwise, all are "allow"
    return {
        "verdict": "allow",
        "reason": None,
        "final_text": results[0]["final_text"] if results else ""
    }
