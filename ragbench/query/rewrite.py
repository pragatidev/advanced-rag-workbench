"""Query rewrite and multi-query. Cheap templates. Live lectures can swap in a model."""

from __future__ import annotations


def rewrite(question: str) -> str:
    q = question.strip()
    if q.lower().startswith("what does error code"):
        return q
    if "growth" in q.lower() and "revenue" in q.lower():
        return q + " sequential quarterly revenue percent"
    return q


def multi_query(question: str) -> list[str]:
    base = rewrite(question)
    return [question, base, f"Passages about: {question}"]
