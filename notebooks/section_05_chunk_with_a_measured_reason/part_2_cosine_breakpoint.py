# %% [markdown]
# # Cut at a cosine percentile
#
# Lab `lab_s5_chunk` / `part_2`.

# %%
"""Cut at a cosine percentile."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunking.semantic import cosine_breakpoint_chunks, cut_mask, pairwise_similarities
from rag.corpus import load_documents
from rag.text import split_sentences

PERCENTILE = 95.0

docs = {d.doc_id: d for d in load_documents()}
doc = docs["filing_q2_2023"]
sents = split_sentences(doc.text)
sims = pairwise_similarities(sents)
cuts = cut_mask(sims, percentile=PERCENTILE)
cutoff = (
    float(np.percentile(np.asarray(sims, dtype=np.float64), 100.0 - PERCENTILE))
    if sims
    else 0.0
)
print("sentences", len(sents), "joints", len(sims))
print("percentile", PERCENTILE, "cutoff", f"{cutoff:.6f}")
print("n_cuts", sum(1 for c in cuts if c))
for i, sim in enumerate(sims):
    mark = "CUT" if cuts[i] else "keep"
    print(f"{i:02d} sim={sim:.4f} {mark}")
    if cuts[i]:
        print(f"{i:02d} L: {sents[i]}")
        print(f"{i:02d} R: {sents[i + 1]}")
chunks = cosine_breakpoint_chunks(doc, percentile=PERCENTILE)
print("semantic_chunks", len(chunks))
