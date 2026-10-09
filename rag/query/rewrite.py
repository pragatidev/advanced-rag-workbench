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


def _word_ngrams(text: str, n: int = 2) -> set[str]:
    toks = [t for t in text.lower().replace("?", " ").replace(":", " ").split() if t]
    if len(toks) < n:
        return {" ".join(toks)} if toks else set()
    return {" ".join(toks[i : i + n]) for i in range(len(toks) - n + 1)}


def ngram_jaccard(a: str, b: str, n: int = 2) -> float:
    sa, sb = _word_ngrams(a, n), _word_ngrams(b, n)
    union = sa | sb
    if not union:
        return 1.0
    return len(sa & sb) / len(union)


def ngram_overlap(queries: list[str], n: int = 2) -> list[tuple[int, int, float]]:
    """Pairwise word-n-gram Jaccard. Near 1.0 means you paid for clones."""
    pairs: list[tuple[int, int, float]] = []
    for i in range(len(queries)):
        for j in range(i + 1, len(queries)):
            pairs.append((i, j, ngram_jaccard(queries[i], queries[j], n)))
    return pairs
