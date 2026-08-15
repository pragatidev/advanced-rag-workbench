"""Cut at a cosine percentile."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunking.semantic import cosine_breakpoint_chunks, pairwise_similarities
from rag.corpus import load_documents
from rag.text import split_sentences

docs = {d.doc_id: d for d in load_documents()}
doc = docs["filing_q2_2023"]
sents = split_sentences(doc.text)
sims = pairwise_similarities(sents)
order = sorted(sims)
cut = order[max(0, int(len(order) * 0.05) - 1)] if order else 0
print("sentences", len(sents), "joints", len(sims))
for i, sim in enumerate(sims):
    mark = "CUT" if sim <= cut else "keep"
    print(f"{i:02d} sim={sim:.3f} {mark}")
chunks = cosine_breakpoint_chunks(doc, percentile=95)
print("semantic_chunks", len(chunks), "recursive would split this doc by headings")
