# Install

Python 3.11 or later. VS Code. Git. **No API key.**

```
cd advanced-rag-workbench
python -m venv .venv
```

Windows:

```
.venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

macOS / Linux:

```
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

Open this folder in VS Code. Open `notebooks/section_02_naive_rag/02.2_build_the_naive_pipeline.py`. Run.

Optional pgvector:

```
docker compose up -d
```

Then run `notebooks/section_02_naive_rag/02.2b_vector_stores.py`.

Optional API generate: copy `.env.example` to `.env`. Never commit `.env`.
