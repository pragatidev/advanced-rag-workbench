# Harness notes

This is a Python project (3.13 recommended, 3.11 to 3.13 supported). The course has 23 sections, numbered 1 to 23 in README.md; folder names are older and keep their own numbers. There are 20 labs with 67 parts under `labs/lab_s*/part_*/`, plus seven scripts in `basics/`. The `# %%` twins of the lab parts are under `notebooks/section_*/`, built by `scripts/make_twins.py`. Retrieval is local. Generate is extractive unless `.env` sets `RAGBENCH_GENERATE=api`; local Ollama needs no key, a hosted door needs `LLM_API_KEY`.

When the owner asks in English:

- Run tests: `pytest` (no key, no model call)
- Walk a lecture: open the matching `labs/lab_s*/part_*/` file (or its notebook twin) and run it from the repo root
- Change a lab part: edit the file under `labs/`, then run `python scripts/make_twins.py`; never edit a twin by hand
- Models: three doors set in `.env` (local Ollama `qwen3:8b` by default, Anthropic, any OpenAI-compatible provider); model ids live in `.env` and `rag/settings.py` only
- Stores: Chroma, FAISS, Qdrant always. pgvector if Docker is up.
- Product: `python app.py` or `from rag import run_ask`
- Do not invent Nike files. Corpus is `data/acme/`.
- Do not turn on web CRAG.
