# Harness notes

This folder is the Advanced RAG workbench. Retrieval is Python. Default generate is extractive. No API key.

When the owner asks in English:

- Run tests: `pytest -q` from this folder (venv on).
- Ask a pipeline: `python -m ragbench ask "<question>" --pipeline naive|hybrid|hyde|graph`
- Compare: `python -m ragbench eval --a naive --b hybrid`
- Do not invent Nike files. Corpus is `data/acme/`. Questions are `eval/questions.jsonl`.
- Do not turn on web CRAG. `WEB_SEARCH_ENABLED` stays false unless they say so.
- A prompt loop is not Self-RAG weights. Say so if you explain S6.
