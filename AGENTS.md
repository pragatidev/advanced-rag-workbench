# Harness notes

This is a Python project. Lecture walks are `notebooks/section_*/S*.py`. Retrieval is local. Default generate is extractive.

When the owner asks in English:

- Run tests: `pytest -q`
- Walk a lecture: open the matching file under `notebooks/` and run it
- Stores: Chroma, FAISS, Qdrant always. pgvector if Docker is up.
- Product: `python app.py` or `from rag import run_ask`
- Do not invent Nike files. Corpus is `data/acme/`.
- Do not turn on web CRAG.
