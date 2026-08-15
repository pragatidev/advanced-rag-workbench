# Harness notes

This is a Python project. Curriculum v1.0: 17 sections, 60 lab parts under `labs/lab_s*/part_*/`. `# %%` twins are `notebooks/section_*/`. Retrieval is local. Default generate is extractive.

When the owner asks in English:

- Run tests: `pytest -q`
- Walk a lecture: open the matching `labs/lab_s*/part_*/` file (or its notebook twin) and run it
- Stores: Chroma, FAISS, Qdrant always. pgvector if Docker is up.
- Product: `python app.py` or `from rag import run_ask`
- Do not invent Nike files. Corpus is `data/acme/`.
- Do not turn on web CRAG.
