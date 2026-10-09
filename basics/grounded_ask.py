"""Look it up, then answer: the TS-999 question through both steps of RAG.

This is the twin of basics/cold_ask.py. There, a model is asked about TS-999 with no
documents and cannot know the answer. Here the same question goes through the two steps
RAG adds:

  1. LOOK IT UP   find the three pieces of data/acme closest to the question
                  (the same look-up as leg [3] of cold_ask.py, so the same three pieces)
  2. ANSWER       send the question and those three pieces to a model, with the
                  workbench's own instructions: answer only from the pieces, cite them

Run from the repo root:
    python basics/grounded_ask.py

Step one needs no key and no model. Step two uses the model your .env points at: local
Ollama with qwen3:8b by default, which needs no key. If no model server is running (or a
hosted door has no key), step two prints a SKIPPED line and the script still exits 0.
"""
from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import get_embedder
from rag.envload import load_dotenv
from rag.llm import SYSTEM, _port_open, _source_blob, chat
from rag.retrieve import dense_search
from rag.settings import Settings

QUESTION = "What does error code TS-999 mean? Answer in one or two sentences."
# chat() waits 90 seconds by default. On a laptop with no GPU, qwen3:8b can take a few
# minutes to load and write its answer, so this script waits up to ten.
TIMEOUT_SECONDS = 600
RULE = "=" * 78


def retrieved(question: str) -> tuple[str, list]:
    """Step one, the same as cold_ask.py leg [3]: 80-word pieces, the real embedder, top 3."""
    docs = load_documents()
    chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
    embedder = get_embedder(Settings.embed_model)
    hits = dense_search(question, chunks, embedder=embedder, k=3)
    return embedder.name, hits


def why_no_model() -> str:
    """Return why step two cannot run, or "" when a model can be asked. Sends nothing."""
    base = Settings.llm_base_url
    if Settings.is_local:
        # A local model needs no key, only a server that is listening.
        address = urlsplit(base)
        if not _port_open(address.hostname, address.port or 80):
            return (
                f"no model server at {base} "
                f"(start Ollama and pull {Settings.llm_model}, then run this again)"
            )
        return ""
    if not Settings.has_api_key:
        return f"no LLM_API_KEY for {base} (set one in .env, or use the local door)"
    return ""


def main() -> int:
    load_dotenv()
    print(RULE)
    print("QUESTION:", QUESTION)
    print(RULE)

    print("\n[STEP 1] LOOK IT UP in data/acme (the same look-up as leg [3] of cold_ask.py)")
    name, hits = retrieved(QUESTION)
    print(f"    embedder: {name}")
    for i, h in enumerate(hits, 1):
        head = " ".join(h.chunk.text.split())[:150]
        print(f"    {i}. {h.chunk.chunk_id}  score {h.score:.3f}")
        print(f"       {head}")

    print("\n[STEP 2] ANSWER from those three pieces (rag/llm.py chat())")
    reason = why_no_model()
    if reason:
        print(f"    SKIPPED: {reason}")
        return 0

    pieces = [h.chunk for h in hits]
    print("    system prompt, as sent:")
    print(f"       | {SYSTEM}")
    print("    user message, as sent (each piece numbered and labelled):")
    for line in _source_blob(QUESTION, pieces).splitlines():
        print(f"       | {line}")
    print(f"\n    asking {Settings.llm_model} (with no GPU this can take a few minutes) ...", flush=True)
    try:
        result = chat(QUESTION, pieces, timeout=TIMEOUT_SECONDS)
    except RuntimeError as exc:  # the model answered with an error, or nothing answered
        print(f"    SKIPPED: {exc}")
        return 0
    except TimeoutError:
        print(f"    SKIPPED: no answer within {TIMEOUT_SECONDS} seconds")
        return 0

    print(f"\n    ANSWER ({result['model']}):")
    for line in result["text"].splitlines() or [""]:
        print(f"    {line}")

    print("\n" + RULE)
    print("The model was told to answer only from the three pieces and to cite them by number.")
    print("Compare it with the cold answers in basics/cold_ask.py.")
    print(RULE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
