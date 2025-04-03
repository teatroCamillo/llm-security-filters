from typing import List
from llm_sf.filters.base_filter import FilterResult

def combine_parallel_results(results: List[FilterResult]) -> FilterResult:
    """
    Bardziej elastyczny mechanizm decyzyjny dla wyników z trybu równoległego.
    Przykład: 
      - jeśli jakikolwiek filtr zwraca block -> block,
      - jeśli żaden nie zablokował, ale któryś sanitize -> sanitize,
      - w innym wypadku -> allow.
    Można tu dodać rozbudowane reguły.
    """
    for r in results:
        if r.verdict == "block":
            return FilterResult(
                verdict="block",
                reason=r.reason, 
                metadata=r.metadata
            )

    sanitize_reasons = []
    for r in results:
        if r.verdict == "sanitize":
            sanitize_reasons.append(r.reason or "sanitize requested")

    if sanitize_reasons:
        return FilterResult(
            verdict="sanitize",
            reason="; ".join(sanitize_reasons)
        )

    # Jeśli nie ma block i nie ma sanitize -> allow
    return FilterResult(verdict="allow")
