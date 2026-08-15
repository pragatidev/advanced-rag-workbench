# %% [markdown]
# # Compare chunkers and pick from the table
#
# Lab `lab_s5_chunk` / `part_3`.

# %%
"""Compare chunkers and pick from the table."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus, token_count
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.eval.metrics import context_recall
from rag.retrieve import bm25_search, dense_search

docs = load_documents()
q_id = "What does error code TS-999 mean?"
q_para = "What was ACME revenue growth in Q2 2023?"
emb = HashEmbedder(semantic_mode=False)
rows = []
for name in ("fixed", "recursive", "semantic"):
    kwargs = {"size": 80, "overlap": 0} if name == "fixed" else {}
    chunks = chunk_corpus(docs, name, **kwargs) if kwargs else chunk_corpus(docs, name)
    dense_id = dense_search(q_id, chunks, embedder=emb, k=4)
    bm25_id = bm25_search(q_id, chunks, k=4)
    dense_p = dense_search(q_para, chunks, embedder=emb, k=4)
    rows.append(
        {
            "chunker": name,
            "n": len(chunks),
            "mean_tokens": round(sum(token_count(c) for c in chunks) / max(len(chunks), 1), 1),
            "bm25_ts999": context_recall(["TS-999"], [h.chunk.text for h in bm25_id]),
            "dense_ts999": context_recall(["TS-999"], [h.chunk.text for h in dense_id]),
            "dense_3pct": context_recall(["revenue grew by 3%"], [h.chunk.text for h in dense_p]),
        }
    )
print(f"{'chunker':12} {'n':>4} {'tok':>6} {'bm25_id':>8} {'dense_id':>8} {'para':>6}")
for r in rows:
    print(f"{r['chunker']:12} {r['n']:4d} {r['mean_tokens']:6.1f} {r['bm25_ts999']:8.2f} {r['dense_ts999']:8.2f} {r['dense_3pct']:6.2f}")
print("keeper: recursive often wins keyword IDs; semantic may win paraphrase")
