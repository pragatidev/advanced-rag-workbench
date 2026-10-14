"""An embedding is a list of numbers that carries meaning: similar ACME sentences land near each other.

Three ACME sentences and two questions go through the embedding model in .env (all-MiniLM-L6-v2,
the same free local model the look-up in cold_ask.py and grounded_ask.py uses; no key, no server).
Each sentence becomes 384 numbers. The script prints the first 6 of each, then how close the
sentences sit, then where each question lands. The second question shares not one word with the
revenue sentences; that is the point.

At the end the same question goes through a word-matching stand-in (HashEmbedder, which only
counts shared words) so you can see what a model that reads meaning adds.

Run from the repo root:
    python basics/embed_two_sentences.py

If the model cannot load (for example with no internet on the very first run, before the model
file is on disk), the script says so and runs the stand-in for everything, so it always finishes.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.embedders import HashEmbedder, cosine, get_embedder
from rag.envload import load_dotenv
from rag.settings import Settings

near_a = "The company's revenue grew by 3% over the previous quarter."
near_b = "Prior quarter revenue was 314 million USD."
far = "Shared passwords are forbidden."
question_a = "How much did ACME make last quarter?"
question_b = "How much money did ACME bring in?"


def pick_embedder():
    """The model named in .env; the word-matching stand-in only if it cannot load."""
    try:
        embedder = get_embedder(Settings.embed_model)
        embedder.embed("warm up")
        return embedder
    except Exception as exc:  # noqa: BLE001 - say why, then keep going offline
        print(f"could not load {Settings.embed_model} ({type(exc).__name__}); using the word-matching stand-in")
        return HashEmbedder()


def main() -> int:
    load_dotenv()
    embedder = pick_embedder()
    print(f"embedder {embedder.name}: {embedder.dim} numbers per sentence (the screen shows the first 6)")
    vec_a, vec_b, vec_far = (embedder.embed(s) for s in (near_a, near_b, far))

    print("near_a", near_a)
    print("  first 6 numbers", [round(float(x), 3) for x in vec_a[:6]])
    print("near_b", near_b)
    print("  first 6 numbers", [round(float(x), 3) for x in vec_b[:6]])
    print("far   ", far)
    print("  first 6 numbers", [round(float(x), 3) for x in vec_far[:6]])
    print("similar pair  ", round(cosine(vec_a, vec_b), 3))
    print("unrelated pair", round(cosine(vec_a, vec_far), 3))
    print("story: the two revenue sentences sit nearer than revenue vs the password rule.")

    for label, question in (("question_a", question_a), ("question_b", question_b)):
        vec_q = embedder.embed(question)
        print(f"{label} {question}")
        print("  vs near_a", round(cosine(vec_q, vec_a), 3))
        print("  vs near_b", round(cosine(vec_q, vec_b), 3))
        print("  vs far   ", round(cosine(vec_q, vec_far), 3))
    print("story: question_b shares no word with the revenue sentences and still lands on them.")

    stand_in = HashEmbedder()
    vec_q = stand_in.embed(question_b)
    print(f"the same question_b on a word-matching stand-in ({stand_in.name}, {stand_in.dim} numbers):")
    print("  vs near_a", round(cosine(vec_q, stand_in.embed(near_a)), 3))
    print("  vs near_b", round(cosine(vec_q, stand_in.embed(near_b)), 3))
    print("  vs far   ", round(cosine(vec_q, stand_in.embed(far)), 3))
    print("story: with no shared word, the stand-in has nothing to hold on to. Meaning is what the model adds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
