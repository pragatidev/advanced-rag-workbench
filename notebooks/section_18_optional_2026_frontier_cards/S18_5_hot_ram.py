# %% [markdown]
# # S18.5 Hot RAM versus object-store vectors
#
# Named frontier card. Not the Monday loop.
# This file prints the card, the tenant namespaces, and a hash gate.
# It does not open a turbopuffer account.

# %%
"""S18.5: print the hot-RAM versus object-store card. Does not install turbopuffer."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.corpus import load_documents
from rag.incremental import DerivedIndex, span_hash

page = (ROOT / "docs" / "mechanisms" / "hot_ram_versus_object_store.md").read_text(encoding="utf-8")

by_tenant: dict[str, list[str]] = {}
for doc in load_documents():
    tenant = str(doc.metadata.get("tenant", "shared"))
    by_tenant.setdefault(tenant, []).append(doc.doc_id)

idx = DerivedIndex()
last_hash: dict[str, str] = {}


def gated_upsert(doc_id: str, text: str) -> str:
    digest = span_hash(text)
    if last_hash.get(doc_id) == digest:
        print("hash gate: skip embed")
        return "skip"
    last_hash[doc_id] = digest
    idx.upsert(doc_id, text)
    print("hash gate: embed")
    return "embed"


span = "TS-999 means the billing ledger rejected a duplicate invoice id."
print("=== not generate tokens only ===")
print("file docs/mechanisms/hot_ram_versus_object_store.md")
print("hot RAM plus 3x SSD")
print("cold S3 plus SSD cache")
print("namespace helix-east", by_tenant.get("helix-east"))
print("namespace shared", sorted(by_tenant.get("shared") or []))
gated_upsert("error_catalog", span)
gated_upsert("error_catalog", span)
print("embed_calls", idx.embed_calls)
print("rule Where the vectors live is a cost lever.")
print()
print("=== hot_ram_versus_object_store.md ===")
print(page.strip())
