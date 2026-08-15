"""Late chunking plus the small-to-big board."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunking.late import late_vectors
from rag.chunkers import chunk_corpus, parent_child
from rag.corpus import load_documents
from rag.embedders import HashEmbedder, cosine
from rag.eval.metrics import context_recall
from rag.retrieve import dense_search

docs = load_documents()
q = "What was ACME revenue growth in Q2 2023?"
gold = ["revenue grew by 3%"]
emb = HashEmbedder(semantic_mode=False)
rec = chunk_corpus(docs, "recursive")
pc = []
for d in docs:
    pc.extend(parent_child(d))
late_chunks, late_vecs = late_vectors(docs, rec, embedder=emb)
qvec = emb.embed(q)
# score late vectors by cosine to the query
order = sorted(
    range(len(late_chunks)),
    key=lambda i: cosine(qvec, late_vecs[i]),
    reverse=True,
)
late_top = [late_chunks[i].text for i in order[:4]]
rows = [
    ("recursive", context_recall(gold, [h.chunk.text for h in dense_search(q, rec, embedder=emb, k=4)])),
    ("parent_child", context_recall(gold, [h.chunk.text for h in dense_search(q, pc, embedder=emb, k=4)])),
    ("late_standin", context_recall(gold, late_top)),
]
print(f"{'method':16} recall@4")
for name, rec_s in rows:
    print(f"{name:16} {rec_s:.2f}")
print("keep-or-kill: late chunking often does not pay on this corpus")
