# Advanced RAG workbench

A normal Python project. Open it in VS Code. Run a lecture notebook like any other `.py` file.

Companion repo for **Advanced RAG Techniques: Hybrid Search to Graph [2026]**.

One corpus (`data/acme/`). One question file (`eval/questions.jsonl`). Real vector stores. Keep the winner. Refuse the rest.

## How you work this (same as a real project)

1. Open this folder in VS Code.
2. Open a lecture file, for example `notebooks/section_02_naive_rag/02.2_build_the_naive_pipeline.py`.
3. Run Cell on each `# %%` block, or Run the file.
4. Open the store folder it wrote (`store/chroma/`, `store/faiss/`, `store/qdrant/`).

The markdown cells are the teaching. The code cells are the run.

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

Then walk lecture 2.2. Then 2.2b (all four local stores).

## Vector stores in this project

| Store | Runs here | What you open |
|---|---|---|
| **Chroma** | yes | `store/chroma/` |
| **FAISS** | yes | `store/faiss/<name>/` |
| **Qdrant** | yes | `store/qdrant/` |
| **pgvector** | yes, optional | Postgres via `docker compose up -d` |
| Pinecone, Weaviate, Milvus | named, not run | need a hosted key |

Same chunks, same vectors, four backends: `notebooks/section_02_naive_rag/02.2b_vector_stores.py`.

Embedding in tests and first clone: `HashEmbedder` (offline). Monday swap: `all-MiniLM-L6-v2` (Chroma ONNX) or `text-embedding-3-small`.

## After the index exists (the product)

A shipped service does not re-type a notebook. It imports a function:

```
from rag import run_ask
result = run_ask("What does error code TS-999 mean?", pipeline="hybrid")
```

Or run the desk:

```
python app.py
```

Open http://127.0.0.1:8787/ or `python examples/ticket_desk.py`.

## Lecture map

See `notebooks/README.md`. Every screen-walk lecture has a file. Concept lectures are animated; they have no notebook.

## Layout

```
data/acme/       teaching corpus
eval/            questions.jsonl
notebooks/       one file per screen-walk lecture
rag/             small library the notebooks import
store/           Chroma / FAISS / Qdrant data (gitignored)
app.py           HTTP product door
docker-compose.yml   optional pgvector
tests/
```

## Honesty

- A prompt loop is not Asai Self-RAG. We ship the loop and say so.
- Anthropic 49 percent / 67 percent figures are theirs, September 2024.
- HyDE invents details on purpose.
- GraphRAG here is a tiny seeded graph, not a Microsoft index.
- Web CRAG stays off unless policy turns it on.
- HashEmbedder is an offline stand-in so TS-999 and pytest work with no download.

```
pytest -q
```

MIT. Built by Pragati Kunwer.
