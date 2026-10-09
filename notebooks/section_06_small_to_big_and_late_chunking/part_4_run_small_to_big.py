# %% [markdown]
# # Late chunking plus the small-to-big board
#
# Lab `lab_s6_s2b` / `part_4`.

# %%
"""Late chunking plus the small-to-big board."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunking.auto_merge import merge_hits
from rag.chunking.late import late_vectors
from rag.chunking.parent_child import expand_to_parent
from rag.chunking.sentence_window import build as build_window
from rag.chunking.sentence_window import expand_window
from rag.chunkers import parent_child
from rag.corpus import load_documents
from rag.embedders import HashEmbedder, cosine
from rag.eval.metrics import context_recall
from rag.retrieve import dense_search

docs = load_documents()
q = "What was ACME revenue growth in Q2 2023?"
gold = ["revenue grew by 3%"]
emb = HashEmbedder(semantic_mode=False)
k = 4

pc = []
win = []
for d in docs:
    pc.extend(parent_child(d, child_size=40))
    win.extend(build_window(d))

pc_hits = expand_to_parent(dense_search(q, pc, embedder=emb, k=k))
win_hits = expand_window(dense_search(q, win, embedder=emb, k=k), win, radius=3)
am_hits = merge_hits(dense_search(q, pc, embedder=emb, k=8), threshold=0.5)[:k]

late_chunks, late_vecs = late_vectors(docs, embedder=emb)
qvec = emb.embed(q)
order = sorted(
    range(len(late_chunks)),
    key=lambda i: cosine(qvec, late_vecs[i]),
    reverse=True,
)
late_top = [late_chunks[i] for i in order[:k]]

pc_texts = [h.chunk.text for h in pc_hits]
win_texts = [h.chunk.text for h in win_hits]
am_texts = [h.chunk.text for h in am_hits]
late_texts = [c.text for c in late_top]
rows = [
    ("parent_child", pc_texts, len(pc)),
    ("sentence_window", win_texts, len(win)),
    ("auto_merge", am_texts, len(pc)),
    ("late_standin", late_texts, len(late_chunks)),
]

print(f"{'method':16} {'recall@4':8} {'mean_chars':10} {'n_index':7} verdict")
for name, texts, n_index in rows:
    rec = context_recall(gold, texts)
    mean_c = int(round(sum(len(t) for t in texts) / max(len(texts), 1)))
    verdict = "KEEP" if rec >= 1.0 else "KILL"
    print(f"{name:16} {rec:<8.2f} {mean_c:<10d} {n_index:<7d} {verdict}")
print("keep-or-kill: late chunking often does not pay on this corpus")
print("late_top4:")
for c in late_top:
    blob = c.text.lower()
    print(f"  {c.chunk_id} ACME {str('acme' in blob)} 3pct {str('revenue grew by 3%' in blob)}")
