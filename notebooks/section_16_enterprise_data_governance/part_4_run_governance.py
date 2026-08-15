# %% [markdown]
# # Audit two tenants, prove the deny
#
# Lab `lab_s16_gov` / `part_4`.

# %%
"""Audit two tenants, prove the deny."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.gov import audit_row, denied_absent, prefilter, redact

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
denied = [c.chunk_id for c in chunks if c.doc_id == "faq"]
for tenant in ("helix-east", "helix-west"):
    allowed_chunks = prefilter(chunks, tenant)
    # pretend these are the prompt chunks
    prompt = [c for c in allowed_chunks if "national id" in c.text.lower() or c.doc_id in {"faq", "privacy", "error_catalog"}][:4]
    texts = [redact(c.text) for c in prompt]
    row = audit_row("How does helix-east reset a password?", prompt, tenant=tenant)
    print(tenant, "ids", row["chunk_ids"], "denied_absent", denied_absent(row, denied) if tenant == "helix-west" else "n/a")
    print("  redacted_any", any("[REDACTED_PII]" in t for t in texts))
print("west must not see faq ids")
west_row = audit_row("q", prefilter(chunks, "helix-west")[:8], tenant="helix-west")
print("proof", denied_absent(west_row, denied))
