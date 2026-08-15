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

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.eval.golden import confirm_tags

docs = load_documents()
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
orphans = [c for c in chunks if "revenue grew by 3%" in c.text.lower()]
orphan = orphans[0]
report = confirm_tags()
board = {
    "orphan": {
        "chunk_id": orphan.chunk_id,
        "contains_acme": "acme" in orphan.text.lower(),
        "contains_q2": "q2" in orphan.text.lower(),
        "has_3_percent": True,
    },
    "golden": report,
}
dest = ROOT / "runs" / "smoke" / "diagnosis_board.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(board, indent=2), encoding="utf-8")
print("orphan contains ACME:", board["orphan"]["contains_acme"])
print("canaries", report["canary_ids"])
print("wrote", dest)
