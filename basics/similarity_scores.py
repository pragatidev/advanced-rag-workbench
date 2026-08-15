"""Cosine similarity is the angle between two embedding arrows, written in plain math."""

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.embedders import HashEmbedder


def cosine(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    n_left = math.sqrt(sum(a * a for a in left))
    n_right = math.sqrt(sum(b * b for b in right))
    return dot / (n_left * n_right)


embedder = HashEmbedder()
names = ["revenue grew 3%", "prior-quarter revenue", "passwords forbidden"]
texts = [
    "The company's revenue grew by 3% over the previous quarter.",
    "Prior quarter revenue was 314 million USD.",
    "Shared passwords are forbidden.",
]
vecs = [embedder.embed(text) for text in texts]
rows = []
for i, left in enumerate(names):
    for j, right in enumerate(names):
        if i < j:
            rows.append((cosine(vecs[i], vecs[j]), left, right))
print("rank  cosine  pair")
for rank, (score, left, right) in enumerate(sorted(rows, reverse=True), start=1):
    print(f"{rank}     {score:.3f}   {left} / {right}")
