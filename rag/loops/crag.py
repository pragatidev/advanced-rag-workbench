"""CRAG-style three-way gate. Web search is a flag. Default off."""

from __future__ import annotations

from rag.retrieve import Hit
from rag.text import tokenize

WEB_SEARCH_ENABLED = False


def grade(query: str, hits: list[Hit], threshold: float = 0.15) -> str:
    """Correct / Incorrect / Ambiguous from query-token coverage of the top hit."""
    if not hits:
        return "Incorrect"
    q = set(tokenize(query))
    if not q:
        return "Ambiguous"
    top = set(tokenize(hits[0].chunk.text))
    cover = len(q & top) / len(q)
    if cover >= 0.5:
        return "Correct"
    if cover < threshold:
        return "Incorrect"
    return "Ambiguous"


def maybe_web(query: str) -> str | None:
    if not WEB_SEARCH_ENABLED:
        return None
    return f"(web search would run for: {query})"
