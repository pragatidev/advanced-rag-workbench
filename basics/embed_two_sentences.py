"""An embedding is a list of numbers that carries meaning — similar ACME sentences land near each other."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.embedders import HashEmbedder, cosine

near_a = "The company's revenue grew by 3% over the previous quarter."
near_b = "Prior quarter revenue was 314 million USD."
far = "Shared passwords are forbidden."

embedder = HashEmbedder()
print("list length", HashEmbedder().dim, "numbers per sentence (the screen shows the first 6)")
vec_a = embedder.embed(near_a)
vec_b = embedder.embed(near_b)
vec_far = embedder.embed(far)
score_near = cosine(vec_a, vec_b)
score_far = cosine(vec_a, vec_far)

print("near_a", near_a)
print("  first 6 numbers", [round(float(x), 3) for x in vec_a[:6]])
print("near_b", near_b)
print("  first 6 numbers", [round(float(x), 3) for x in vec_b[:6]])
print("far   ", far)
print("  first 6 numbers", [round(float(x), 3) for x in vec_far[:6]])
print("similar pair", round(score_near, 3))
print("unrelated pair", round(score_far, 3))
print("story: the two revenue sentences sit nearer than revenue vs the password rule.")

question = "How much did ACME make last quarter?"
vec_q = embedder.embed(question)
print("question", question)
print("  vs near_a", round(cosine(vec_q, vec_a), 3))
print("  vs near_b", round(cosine(vec_q, vec_b), 3))
print("  vs far   ", round(cosine(vec_q, vec_far), 3))
print("story: the question never says revenue, and it still lands nearest the revenue sentences.")
