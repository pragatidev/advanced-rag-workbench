"""Tiny labeled metrics. Not a RAGAS install. Faithfulness here is extractive support."""

from __future__ import annotations


def _norm(text: str) -> str:
    return " ".join((text or "").lower().split())


def context_recall(gold_spans: list[str], retrieved_texts: list[str]) -> float:
    if not gold_spans:
        return 1.0
    blob = _norm(" ".join(retrieved_texts))
    hits = sum(1 for span in gold_spans if _norm(span) in blob)
    return hits / len(gold_spans)


def needles_hit(needles: list[str], retrieved_texts: list[str]) -> float:
    if not needles:
        return 1.0
    blob = _norm(" ".join(retrieved_texts))
    hits = sum(1 for n in needles if _norm(n) in blob)
    return hits / len(needles)


def faithfulness(answer: str, retrieved_texts: list[str]) -> float:
    if answer.startswith("REFUSE"):
        return 1.0
    blob = _norm(" ".join(retrieved_texts))
    tokens = [t for t in _norm(answer).split() if len(t) > 2]
    if not tokens:
        return 0.0
    supported = sum(1 for t in tokens if t in blob)
    return supported / len(tokens)
