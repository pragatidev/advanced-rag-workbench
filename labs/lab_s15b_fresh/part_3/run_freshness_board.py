"""One board: tombstone proof plus mixed-space fail plus cutover switch."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.corpus import load_documents
from rag.cutover import DualColumnIndex, VersionedEmbedder
from rag.embed import ToyEmbedder, cosine
from rag.incremental import DerivedIndex, stable_chunk_key

OLD_SENTENCE = "Customer email, phone, and national id are PII."
NEW_SENTENCE = "Customer email, phone, and date of birth are PII."

CHUNKS = [
    ("policy", "Retention is seven days. That line is the live policy."),
    ("warehouse_00", "Warehouse throughput improved. Marketing spend was steady."),
    ("warehouse_01", "Seats by region east west north south. Padding about capacity."),
    ("error_catalog", "TS-999 means the billing ledger rejected a duplicate invoice ID."),
    ("privacy", "Customer email, phone, and national id are PII. Redact national id."),
    ("access", "Least privilege. Support may read email. National id stays redacted."),
    ("faq", "Reset the token, then retry the invoice. Do not invent a new id."),
    ("kpis", "Q2 seats east 4100 west 3900 north 2420 south 2000."),
]

QUERY = "retention is seven days"
SAME = "Retention is seven days. That line is the live policy."


def first_body_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped
    return text[:80]


idx = DerivedIndex(ToyEmbedder(semantic_mode=False))
docs = load_documents()
privacy = next(doc for doc in docs if doc.doc_id == "privacy")
if OLD_SENTENCE not in privacy.text:
    raise SystemExit("expected ACME privacy sentence missing")

for doc in docs:
    idx.upsert(doc.doc_id, doc.text)

old_id = stable_chunk_key(privacy.doc_id, privacy.text)
new_text = privacy.text.replace(OLD_SENTENCE, NEW_SENTENCE, 1)
before = idx.embed_calls
new_id = idx.upsert(privacy.doc_id, new_text)
idx.tombstone(old_id)
stale_hits = idx.retrieve(OLD_SENTENCE, k=3)
stale_ids = [hit[0] for hit in stale_hits]
stale_present = old_id in stale_ids

print("=== BOARD tombstone ===")
print("source_docs", len(docs))
print("index_live", sum(1 for row in idx.rows.values() if row.live))
print("changed_file", privacy.path)
print("files_to_embedder", idx.embed_calls - before)
print("old_id", old_id)
print("new_id", new_id)
print("query", OLD_SENTENCE)
print("stale_id_present", stale_present)
print("top_id", stale_hits[0][0] if stale_hits else "NONE")
print("top_text", first_body_line(stale_hits[0][1]) if stale_hits else "NONE")

v1 = VersionedEmbedder("v1")
v3 = VersionedEmbedder("v3")
dual = DualColumnIndex()
dual.fill_column("v1", CHUNKS, v1)
dual.fill_column("v3", CHUNKS, v3)
dual.shadow = True
hits_same, meta_same = dual.retrieve(QUERY, "v1", column="v1", k=3)
hits_mix, meta_mix = dual.retrieve(QUERY, "v3", column="v1", k=3)
v1_v3 = round(float(cosine(v1.embed(SAME), v3.embed(SAME))), 4)

print()
print("=== BOARD mixed space ===")
print("text", SAME)
print("v1_vs_v3_cosine", v1_v3)
print("query", QUERY)
print("query_version", meta_mix["query_version"])
print("column", meta_mix["column"])
print("mixed", meta_mix["mixed"])
print("error_raised", meta_mix["error_raised"])
print("top_id", hits_mix[0][0])
print("top_score", round(hits_mix[0][2], 4))
print("top_text", hits_mix[0][1])
print("same_space_top_id", hits_same[0][0])
print("mixed_matches_same_space", hits_mix[0][0] == hits_same[0][0])

print()
print("=== BOARD cutover switch ===")
print("v1_rows", len(dual.columns["v1"]))
print("v3_rows", len(dual.columns["v3"]))
print("live_before", dual.live)
flipped = dual.flip("v3")
print("flip", flipped)
print("live_after", dual.live)
hits_live, meta_live = dual.retrieve(QUERY, "v3", k=1)
print("query_version", meta_live["query_version"])
print("column", meta_live["column"])
print("mixed", meta_live["mixed"])
print("error_raised", meta_live["error_raised"])
print("top_id", hits_live[0][0])
print("top_score", round(hits_live[0][2], 4))
print("top_text", hits_live[0][1])

stale_gone = not stale_present
mixed_fails = bool(meta_mix["mixed"]) and (not bool(meta_mix["error_raised"])) and (
    hits_mix[0][0] != hits_same[0][0]
)
switch_ok = dual.live == "v3" and hits_live[0][0] == "policy" and (not bool(meta_live["mixed"]))

print()
print("=== BOARD verdict ===")
print("stale_sentence_gone", stale_gone)
print("mixed_space_fails", mixed_fails)
print("switch_flipped", switch_ok)
