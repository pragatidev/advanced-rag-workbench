# Harness notes

This folder is the Advanced RAG workbench. Retrieval is Python. Default generate is extractive. No API key.

When the owner asks in English:

- Run tests: `pytest -q` from this folder (venv on).
- Screen walk: `python labs/02_naive_pipeline.py` then open `store/naive/manifest.json` (embedder name + chunker).
- Build / inspect store: `python -m ragbench index naive` / `python -m ragbench inspect naive`
- Product invoke: import `run_ask` from `ragbench`, or `python -m ragbench serve` (POST /ask, desk at /).
- Ticket-shaped demo: `python examples/ticket_desk.py`
- Lab CLI: `python -m ragbench ask "<question>" --pipeline naive|hybrid|hyde|graph`
- Compare: `python -m ragbench eval --a naive --b hybrid`
- ACME questions: use the `ask-acme` skill (retrieve first, cite chunk ids).
- Do not invent Nike files. Corpus is `data/acme/`. Questions are `eval/questions.jsonl`.
- Do not turn on web CRAG. `WEB_SEARCH_ENABLED` stays false unless they say so.
- A prompt loop is not Self-RAG weights. Say so if you explain S6.
