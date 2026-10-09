# %% [markdown]
# # BM25 hits the token
#
# Lab `lab_s7_hybrid` / `part_2`.

# %%
"""BM25 hits the token."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.retrieve import bm25_search
from rag.text import tokenize

QUESTION = "What does error code TS-999 mean?"

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
print("chunks", len(chunks))
print("query_tokens", tokenize(QUESTION))
ranked = bm25_search(QUESTION, chunks, k=len(chunks))
print("bm25 top:")
for h in ranked[:5]:
    flag = "TS-999" in h.chunk.text
    print(f"  {h.score:.3f} ts999={flag} {h.chunk.chunk_id}")
    print("   ", h.chunk.text[:140].replace("\n", " "))
print("BM25 top has TS-999", "TS-999" in ranked[0].chunk.text)
gen_hit = None
ts_hit = None
gen_rank = None
ts_rank = None
for i, h in enumerate(ranked, 1):
    if gen_rank is None and "error codes in general" in h.chunk.text.lower():
        gen_rank = i
        gen_hit = h
    if ts_rank is None and h.chunk.chunk_id == "error_catalog:rec:2":
        ts_rank = i
        ts_hit = h
print("ts999_rank", ts_rank, "score", round(ts_hit.score, 3), "of", len(ranked))
print("  ", ts_hit.chunk.text.replace("\n", " ")[:180])
print("general_guidance_rank", gen_rank, "score", round(gen_hit.score, 3))
print("  ", gen_hit.chunk.text.replace("\n", " ")[:180])
assert "TS-999" in ranked[0].chunk.text
