"""Change one ACME file, upsert, tombstone the old ids."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.corpus import load_documents
from rag.embed import ToyEmbedder
from rag.incremental import DerivedIndex, stable_chunk_key

OLD_SENTENCE = "Customer email, phone, and national id are PII."
NEW_SENTENCE = "Customer email, phone, and date of birth are PII."


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

print("=== warehouse ===")
print("source_docs", len(docs))
print("index_live", sum(1 for row in idx.rows.values() if row.live))
print("changed_file", privacy.path)
print("old_id", old_id)

new_text = privacy.text.replace(OLD_SENTENCE, NEW_SENTENCE, 1)
before = idx.embed_calls
new_id = idx.upsert(privacy.doc_id, new_text)
idx.tombstone(old_id)

print()
print("=== change one ACME file ===")
print("old_line", OLD_SENTENCE)
print("new_line", NEW_SENTENCE)
print("files_to_embedder", idx.embed_calls - before)
print("embed_calls_this_change", idx.embed_calls - before)
print("new_id", new_id)
print("tombstoned", 1)
print("live_after", sum(1 for row in idx.rows.values() if row.live))

print()
print("=== retrieve stale ===")
query = OLD_SENTENCE
hits = idx.retrieve(query, k=3)
ids = [hit[0] for hit in hits]
print("query", query)
print("stale_id_present", old_id in ids)
print("top_id", hits[0][0] if hits else "NONE")
print("top_text", first_body_line(hits[0][1]) if hits else "NONE")
