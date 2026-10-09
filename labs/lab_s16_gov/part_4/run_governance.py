"""Audit two tenants, prove the deny.

The audit is chunk ids and hashes. The final sentence is not the audit.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.generate import generate
from rag.gov import audit_row, denied_absent, prefilter, redact
from rag.retrieve import bm25_search

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
query = "How do I reset my password?"
k = 3
denied = [c.chunk_id for c in chunks if c.doc_id == "faq"]
rows = {}

print("=== two tenants ===")
print("query", query)
print("denied", denied)

for tenant in ("helix-east", "helix-west"):
    allowed_chunks = prefilter(chunks, tenant)
    hits = bm25_search(query, allowed_chunks, k=k)
    prompt = [h.chunk for h in hits]
    sent = [redact(c.text) for c in prompt]
    row = audit_row(query, prompt, tenant=tenant)
    answer = generate(query, prompt)
    rows[tenant] = row
    print()
    print("===", tenant, "===")
    print("tenant", row["tenant"])
    print("question_hash", row["question_hash"])
    print("chunk_ids", row["chunk_ids"])
    print("chunk_hashes", row["chunk_hashes"])
    print("model", row["model"])
    print("denied_absent", denied_absent(row, denied))
    print("redacted_any", any("[REDACTED_PII]" in t for t in sent))
    print("answer", answer)

print()
print("=== proof ===")
print("west must not see faq ids")
print("proof", denied_absent(rows["helix-west"], denied))
