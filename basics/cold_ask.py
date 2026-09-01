"""Ask about a private fact three ways, and read the three answers.

This is the demo behind "why a model cannot answer from your files".

  1. COLD, hosted    a frontier model, no documents, asked the way anyone would ask it
  2. COLD, local     a model on your own machine, same question, no documents
  3. RETRIEVED       the same question through this workbench, with the corpus attached

The point is not that one model is better. Both cold answers fail the same way, because
TS-999 was never in any model's training data: it lives in one file in data/acme/. That is
what retrieval fixes, and it is why a bigger model is not the answer.

Run:
    python basics/cold_ask.py

Needs no key for the local leg. The hosted leg is skipped with a printed note if LLM_API_KEY
is unset, so this script always runs.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import get_embedder
from rag.envload import load_dotenv
from rag.retrieve import dense_search
from rag.settings import Settings

QUESTION = "What does error code TS-999 mean? Answer in one or two sentences."
LOCAL_BASE = "http://localhost:11434/v1"
LOCAL_MODEL = "llama3.2:3b"
RULE = "=" * 78


def _post(url: str, headers: dict, body: dict, timeout: int = 90) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST"
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def cold_anthropic(question: str) -> tuple[str, str]:
    """A plain ask. No system prompt, no sources: exactly how a person would ask it."""
    payload = _post(
        Settings.llm_base_url.rstrip("/") + "/v1/messages",
        {
            "Content-Type": "application/json",
            "x-api-key": Settings.api_key,
            "anthropic-version": "2023-06-01",
        },
        {
            "model": Settings.llm_model,
            "max_tokens": 300,
            "messages": [{"role": "user", "content": question}],
        },
    )
    parts = payload.get("content") or []
    text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
    return text.strip(), Settings.llm_model


def cold_local(question: str) -> tuple[str, str]:
    payload = _post(
        LOCAL_BASE + "/chat/completions",
        {"Content-Type": "application/json", "Authorization": "Bearer ollama"},
        {
            "model": LOCAL_MODEL,
            "messages": [{"role": "user", "content": question}],
            "temperature": 0,
        },
    )
    return payload["choices"][0]["message"]["content"].strip(), LOCAL_MODEL


def retrieved(question: str) -> tuple[str, list]:
    docs = load_documents()
    chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
    embedder = get_embedder(Settings.embed_model)
    hits = dense_search(question, chunks, embedder=embedder, k=3)
    return embedder.name, hits


def main() -> int:
    load_dotenv()
    print(RULE)
    print("QUESTION:", QUESTION)
    print(RULE)

    print("\n[1] COLD, hosted frontier model, no documents")
    if Settings.has_api_key:
        try:
            text, model = cold_anthropic(QUESTION)
            print(f"    model: {model}")
            print(f"    {text}")
        except urllib.error.HTTPError as exc:
            print(f"    HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:200]}")
    else:
        print("    skipped: LLM_API_KEY is not set. The other two legs still run.")

    print("\n[2] COLD, local model on this machine, no documents")
    try:
        text, model = cold_local(QUESTION)
        print(f"    model: {model}")
        print(f"    {text}")
    except Exception as exc:  # noqa: BLE001 - a missing Ollama is a normal state here
        print(f"    skipped: no local model answered on {LOCAL_BASE} ({type(exc).__name__})")

    print("\n[3] RETRIEVED from data/acme, the same question")
    name, hits = retrieved(QUESTION)
    print(f"    embedder: {name}")
    for i, h in enumerate(hits, 1):
        head = " ".join(h.chunk.text.split())[:150]
        print(f"    {i}. {h.chunk.chunk_id}  score {h.score:.3f}")
        print(f"       {head}")

    print("\n" + RULE)
    print("Both cold answers failed the same way. TS-999 is not in any model's weights.")
    print("It is one line in data/acme/runbooks/error_catalog.md, and retrieval found it.")
    print(RULE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
