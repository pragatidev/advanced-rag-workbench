# %% [markdown]
# # Find the orphan 3 percent chunk
#
# Lab `lab_s4_diagnose` / `part_1`.

# %%
"""Find the orphan 3 percent chunk."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents

docs = load_documents()
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
orphans = [c for c in chunks if "revenue grew by 3%" in c.text.lower()]
assert orphans
for c in orphans:
    low = c.text.lower()
    print("chunk_id", c.chunk_id)
    print("contains ACME:", "acme" in low)
    print("contains Q2:", "q2" in low)
    print(c.text)
    print("---")
