# %% [markdown]
# # Bake off two embedders on the same chunks
#
# Lab `lab_s4_diagnose` / `part_3`.

# %%
"""Bake off two embedders on the same chunks."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import time

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.eval.golden import load_golden
from rag.eval.metrics import context_recall
from rag.retrieve import dense_search

docs = load_documents()
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
questions = [r for r in load_golden() if r.get("gold_spans")]
pair = [
    ("HashEmbedder-semantic", HashEmbedder(semantic_mode=True)),
    ("HashEmbedder-lexical", HashEmbedder(semantic_mode=False)),
]
print("same chunks", len(chunks), "questions", len(questions))
print("monday swap: nomic-embed-text vs text-embedding-3-large")
for name, emb in pair:
    t0 = time.perf_counter()
    _ = emb.encode([c.text for c in chunks])
    embed_ms = (time.perf_counter() - t0) * 1000
    recalls = []
    for row in questions:
        hits = dense_search(row["question"], chunks, embedder=emb, k=4)
        recalls.append(context_recall(row["gold_spans"], [h.chunk.text for h in hits]))
    mean = sum(recalls) / len(recalls)
    print(f"{name:24} recall@4={mean:.3f} embed_ms={embed_ms:.1f}")
