"""Count what you send: three pieces against the whole pile, and a window smaller than the pile.

The same TS-999 question goes to the free local model three times, and each time the model's own
meter is printed: how many tokens it read, and how many it wrote.

  1. THREE PIECES   the three pieces retrieval finds (the same look-up as grounded_ask.py)
  2. WHOLE PILE     every piece of data/acme, the way you would paste the whole folder in
  3. SMALL WINDOW   the whole pile again, with the model's window set to 512 tokens on purpose,
                    smaller than the pile, so you can see what happens when a pile does not fit

Run from the repo root:
    python basics/count_what_you_send.py

It needs the local model (Ollama with qwen3:8b) and no key. It asks the local door in .env, or
Ollama on localhost:11434 when .env names a hosted door or none, because the meter and the window
are Ollama's own (its /api/chat and /api/ps). With no Ollama answering it prints SKIPPED and still
exits 0. On a laptop with no GPU each ask can take a minute or two.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import get_embedder
from rag.envload import load_dotenv
from rag.llm import SYSTEM, _port_open, _source_blob
from rag.retrieve import dense_search
from rag.settings import DEFAULT_LLM_BASE_URL, DEFAULT_LLM_MODEL, Settings

QUESTION = "What does error code TS-999 mean? Answer in one or two sentences."
SMALL_WINDOW = 512
TIMEOUT_SECONDS = 600
RULE = "=" * 78


def pieces() -> tuple[list, list]:
    """Every 80-word piece of data/acme, and the three the look-up finds (as in grounded_ask.py)."""
    chunks = chunk_corpus(load_documents(), "fixed", size=80, overlap=0)
    hits = dense_search(QUESTION, chunks, embedder=get_embedder(Settings.embed_model), k=3)
    return chunks, [h.chunk for h in hits]


def ollama_door() -> tuple[str, str]:
    """Ollama's own address (no /v1) and the model: the local door in .env, else Ollama's default."""
    base, model = (Settings.llm_base_url, Settings.llm_model) if Settings.is_local else (
        DEFAULT_LLM_BASE_URL, DEFAULT_LLM_MODEL)
    address = urlsplit(base)
    return f"{address.scheme}://{address.netloc}", model


def _call(url: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        return json.loads(resp.read().decode("utf-8"))


def ask(server: str, model: str, user: str, window: int | None = None) -> dict:
    """One ask on Ollama's /api/chat: the workbench's rule, then the question and the pieces."""
    options = {"temperature": 0}
    if window:
        options["num_ctx"] = window
    return _call(server + "/api/chat", {
        "model": model,
        "stream": False,
        "options": options,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
    })


def window_now(server: str, model: str) -> int | None:
    """The window Ollama gave the loaded model, from /api/ps."""
    for row in _call(server + "/api/ps").get("models", []):
        if row.get("name") == model or row.get("model") == model:
            return row.get("context_length")
    return None


def show(step: str, label: str, sent: list, total: int, reply: dict) -> None:
    words = len(_source_blob(QUESTION, sent).split())
    print(f"\n[{step}] {label}: {len(sent)} of {total} pieces, {words} words")
    print(f"    the model read:  {reply.get('prompt_eval_count')} tokens")
    print(f"    the model wrote: {reply.get('eval_count')} tokens (its thinking and its answer)")
    print("    ANSWER:")
    for line in (reply.get("message", {}).get("content") or "").strip().splitlines() or [""]:
        print(f"    {line}")


def main() -> int:
    load_dotenv()
    print(RULE)
    print("QUESTION:", QUESTION)
    print(RULE)
    every, three = pieces()
    server, model = ollama_door()
    address = urlsplit(server)
    if not _port_open(address.hostname, address.port or 80):
        print(f"\nSKIPPED: no model server at {server} (start Ollama and pull {model}, then run this again)")
        return 0
    print(f"\nasking {model} on {server}, three times (with no GPU each can take a minute or two) ...",
          flush=True)
    try:
        r1 = ask(server, model, _source_blob(QUESTION, three))
        default_window = window_now(server, model)
        show("1", "THREE PIECES", three, len(every), r1)
        r2 = ask(server, model, _source_blob(QUESTION, every))
        show("2", "WHOLE PILE", every, len(every), r2)
        r3 = ask(server, model, _source_blob(QUESTION, every), window=SMALL_WINDOW)
        show("3", f"WHOLE PILE, WINDOW SET TO {SMALL_WINDOW} TOKENS", every, len(every), r3)
    except Exception as exc:  # noqa: BLE001 - LM Studio, an old Ollama, or a timeout: say so and stop
        print(f"\nSKIPPED: Ollama's /api/chat did not answer on {server} ({type(exc).__name__}: {exc})")
        return 0

    print("\n" + RULE)
    sent, small = r2.get("prompt_eval_count"), r3.get("prompt_eval_count")
    print(f"Your machine gave {model} a window of {default_window} tokens.")
    print(f"The whole pile cost {sent} tokens a question; the three pieces cost {r1.get('prompt_eval_count')}.")
    if sent and small and small < sent:
        print(f"With a {SMALL_WINDOW}-token window the model read {small} of those {sent} tokens,")
        print("and nothing warned you. Read answer [3] again: what question is it answering?")
    print(RULE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
