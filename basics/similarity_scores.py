"""Cosine similarity is the angle between two embedding arrows, written in plain math.

The three ACME sentences from embed_two_sentences.py go through the embedding model in .env
(all-MiniLM-L6-v2, free, local, no key). Then cosine is computed by hand, four lines, and the three
pairs are ranked. The norm lines show each arrow's length, so you can see the angle is what ranks
them, not the length.

Run from the repo root:
    python basics/similarity_scores.py

If the model cannot load, the script says so and uses the word-matching stand-in, so it always finishes.
"""

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.embedders import HashEmbedder, get_embedder
from rag.envload import load_dotenv
from rag.settings import Settings


def cosine(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    n_left = math.sqrt(sum(a * a for a in left))
    n_right = math.sqrt(sum(b * b for b in right))
    return dot / (n_left * n_right)


def pick_embedder():
    try:
        embedder = get_embedder(Settings.embed_model)
        embedder.embed("warm up")
        return embedder
    except Exception as exc:  # noqa: BLE001
        print(f"could not load {Settings.embed_model} ({type(exc).__name__}); using the word-matching stand-in")
        return HashEmbedder()


names = ["revenue grew 3%", "prior-quarter revenue", "passwords forbidden"]
texts = [
    "The company's revenue grew by 3% over the previous quarter.",
    "Prior quarter revenue was 314 million USD.",
    "Shared passwords are forbidden.",
]


def main() -> int:
    load_dotenv()
    embedder = pick_embedder()
    print(f"embedder {embedder.name}: {embedder.dim} numbers per sentence")
    vecs = [embedder.embed(text) for text in texts]
    for name, vec in zip(names, vecs):
        print("norm", round(math.sqrt(sum(float(x) * float(x) for x in vec)), 3), name)
    rows = []
    for i, left in enumerate(names):
        for j, right in enumerate(names):
            if i < j:
                rows.append((cosine(vecs[i], vecs[j]), left, right))
    print("rank  cosine  pair")
    for rank, (score, left, right) in enumerate(sorted(rows, reverse=True), start=1):
        print(f"{rank}     {score:.3f}   {left} / {right}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
