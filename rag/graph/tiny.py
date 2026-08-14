"""Tiny GraphRAG-style community summary. Not a Microsoft index. Cost is on the returned dict."""

from __future__ import annotations

from collections import defaultdict

from rag.corpus import load_documents
from rag.text import tokenize

# Seed communities so the global question has a real answer without an LLM extract.
_COMMUNITIES = {
    "revenue": "sequential revenue reporting",
    "billing": "billing integrity",
    "access": "least-privilege access",
    "privacy": "PII minimization",
}


def build() -> dict:
    docs = load_documents()
    entities: dict[str, set[str]] = defaultdict(set)
    for doc in docs:
        toks = set(tokenize(doc.text))
        for key in _COMMUNITIES:
            if key in toks or (key == "privacy" and "pii" in toks):
                entities[key].add(doc.doc_id)
    summary = (
        "Main themes: sequential revenue reporting, billing integrity, "
        "least-privilege access, and PII minimization."
    )
    return {
        "nodes": sorted(entities),
        "members": {k: sorted(v) for k, v in entities.items()},
        "community_summary": summary,
        "index_cost": {
            "llm_extract_calls": 0,
            "note": "seeded toy graph. a real GraphRAG index would extract entities with an LLM.",
        },
    }


def answer_global(question: str) -> dict:
    g = build()
    return {
        "pipeline": "graph_tiny",
        "question": question,
        "answer": g["community_summary"],
        "hits": [{"chunk_id": "community:root", "score": 1.0, "text": g["community_summary"], "doc_id": "graph"}],
        "graph": g,
    }
