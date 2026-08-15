# Install

Python 3.11 or 3.12. VS Code. Git. **No API key.**

Preferred:

```
uv sync
copy .env.example .env
uv run pytest -q
```

Fallback:

```
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

Open this folder in VS Code. Open `labs/lab_s2_env/part_1/setup_clone.py` or `notebooks/section_02_set_up_any_provider_and_local/`.

Optional pgvector:

```
docker compose up -d
```

Then run `labs/lab_s3_naive/part_3/compare_stores.py`.

Optional extras:

```
uv sync --extra local-rerank
uv sync --extra docling
uv sync --extra pgvector
```

Optional API generate: copy `.env.example` to `.env`. Set `DASHSCOPE_API_KEY` or point `LLM_BASE_URL` at Ollama (`http://localhost:11434/v1`) or LM Studio (`http://localhost:1234/v1`). Never commit `.env`.
