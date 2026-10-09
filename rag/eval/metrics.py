"""Tiny labeled metrics. Not a RAGAS install. Faithfulness here is extractive support."""

from __future__ import annotations

import math


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


def precision_at_k(rels: list[int], k: int) -> float:
    """Fraction of the top k that are labeled relevant."""
    if k <= 0:
        return 0.0
    top = rels[:k]
    return sum(int(r) for r in top) / k


def recall_at_k(rels: list[int], k: int) -> float:
    """Fraction of all labeled relevant items that landed in the top k."""
    gold = sum(int(r) for r in rels)
    if gold == 0:
        return 1.0
    return sum(int(r) for r in rels[:k]) / gold


def mrr(rels: list[int]) -> float:
    """One over the rank of the first relevant item. Zero if none."""
    for i, r in enumerate(rels, start=1):
        if int(r):
            return 1.0 / i
    return 0.0


def average_precision(rels: list[int], n_relevant: int | None = None) -> float:
    """Average of precision at each relevant rank, divided by labeled gold count."""
    gold = int(n_relevant) if n_relevant is not None else sum(int(r) for r in rels)
    if gold <= 0:
        return 0.0
    hits = 0
    acc = 0.0
    for i, r in enumerate(rels, start=1):
        if int(r):
            hits += 1
            acc += hits / i
    return acc / gold


def dcg_at_k(rels: list[int], k: int) -> float:
    score = 0.0
    for i, r in enumerate(rels[:k], start=1):
        if int(r):
            score += 1.0 / math.log2(i + 1)
    return score


def ndcg_at_k(rels: list[int], k: int) -> float:
    """Binary nDCG. Ideal ranking packs the golds at the top."""
    gain = dcg_at_k(rels, k)
    ideal = sorted((int(r) for r in rels), reverse=True)
    idcg = dcg_at_k(ideal, k)
    if idcg == 0:
        return 0.0
    return gain / idcg
