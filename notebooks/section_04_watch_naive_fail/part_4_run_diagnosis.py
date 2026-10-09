# %% [markdown]
# # The diagnosis board
#
# Lab `lab_s4_diagnose` / `part_4`.

# %%
"""The diagnosis board."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import json
import time

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.eval.golden import confirm_tags, load_golden
from rag.eval.metrics import context_recall
from rag.retrieve import dense_search

docs = load_documents()
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
orphans = [c for c in chunks if "revenue grew by 3%" in c.text.lower()]
orphan = orphans[0]
low = orphan.text.lower()
orphan_block = {
    "chunk_id": orphan.chunk_id,
    "contains_acme": "acme" in low,
    "contains_q2": "q2" in low,
    "has_3_percent": True,
}

report = confirm_tags()
canary_block = {
    "n": report["n"],
    "n_canaries": report["n_canaries"],
    "canary_ids": report["canary_ids"],
    "ok": report["ok"],
}

questions = [r for r in load_golden() if r.get("gold_spans")]
pair = [
    ("HashEmbedder-semantic", HashEmbedder(semantic_mode=True)),
    ("HashEmbedder-lexical", HashEmbedder(semantic_mode=False)),
]
bake_rows = []
for name, emb in pair:
    t0 = time.perf_counter()
    _ = emb.encode([c.text for c in chunks])
    embed_ms = (time.perf_counter() - t0) * 1000
    recalls = []
    for row in questions:
        hits = dense_search(row["question"], chunks, embedder=emb, k=4)
        recalls.append(context_recall(row["gold_spans"], [h.chunk.text for h in hits]))
    mean = sum(recalls) / len(recalls)
    bake_rows.append(
        {
            "name": name,
            "recall_at_4": round(mean, 3),
            "embed_ms": round(embed_ms, 1),
        }
    )
left, right = bake_rows[0]["recall_at_4"], bake_rows[1]["recall_at_4"]
if left > right:
    winner = bake_rows[0]["name"]
elif right > left:
    winner = bake_rows[1]["name"]
else:
    winner = "TIE"
embedder_block = {
    "same_chunks": len(chunks),
    "questions": len(questions),
    "rows": bake_rows,
    "winner": winner,
}

board = {
    "orphan": orphan_block,
    "canaries": canary_block,
    "embedder": embedder_block,
}
dest = ROOT / "runs" / "smoke" / "diagnosis_board.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(board, indent=2), encoding="utf-8")

print("=== ORPHAN ===")
print("chunk_id", orphan_block["chunk_id"])
print("contains ACME:", orphan_block["contains_acme"])
print("contains Q2:", orphan_block["contains_q2"])
print("has_3_percent:", orphan_block["has_3_percent"])
print("=== CANARIES ===")
print("n", canary_block["n"])
print("n_canaries", canary_block["n_canaries"])
print("canary_ids", canary_block["canary_ids"])
print("ok", canary_block["ok"])
print("=== EMBEDDER ===")
print("same chunks", embedder_block["same_chunks"], "questions", embedder_block["questions"])
for row in bake_rows:
    print(f"{row['name']:24} recall@4={row['recall_at_4']:.3f} embed_ms={row['embed_ms']:.1f}")
print("winner", winner)
print("wrote", dest.relative_to(ROOT).as_posix())
