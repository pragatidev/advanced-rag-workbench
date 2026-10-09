"""Hybrid, context, rerank, and pack."""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus, contextualize
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.eval.metrics import context_recall
from rag.rerank import pack_ends, rerank_cross_encoder
from rag.retrieve import bm25_search, dense_search, rrf_fuse

docs = load_documents()
raw = chunk_corpus(docs, "recursive")
ctx = [contextualize(c) for c in raw]
q = "What does error code TS-999 mean?"
emb = HashEmbedder(semantic_mode=True)
gold = ["TS-999"]

t_naive = time.perf_counter()
naive_hits = dense_search(q, raw, embedder=emb, k=4)
naive_ms = (time.perf_counter() - t_naive) * 1000.0
naive_recall = context_recall(gold, [h.chunk.text for h in naive_hits])

t0 = time.perf_counter()
fused = rrf_fuse([dense_search(q, ctx, embedder=emb, k=10), bm25_search(q, ctx, k=10)], top_n=10)
ranked, backend = rerank_cross_encoder(q, fused, keep=4)
packed = pack_ends(ranked)
stack_ms = (time.perf_counter() - t0) * 1000.0
recall = context_recall(gold, [h.chunk.text for h in packed])

print("backend", backend)
print("packed", [h.chunk.chunk_id for h in packed])
print("naive_recall@k", naive_recall)
print("recall@k", recall)
print("lift vs dense-only", recall >= naive_recall)
print(f"naive_ms {naive_ms:.1f}")
print(f"stack_ms {stack_ms:.1f}")
