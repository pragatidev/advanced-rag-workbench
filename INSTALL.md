# Install

Python 3.13 (recommended; 3.11 and 3.12 also work), VS Code and Git. **No API key.**

Clone the repo and work from its folder:

```
git clone https://github.com/pragatidev/advanced-rag-workbench.git
cd advanced-rag-workbench
```

## With uv (preferred)

```
uv sync
copy .env.example .env
uv run pytest
```

On macOS and Linux, use `cp` instead of `copy`.

## With pip

Windows, Command Prompt:

```
py -3.13 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
pytest
```

Windows, PowerShell:

```
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
pytest
```

If PowerShell says running scripts is disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then activate again.

macOS / Linux:

```
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest
```

No `py` or `python3.13` command? Any Python 3.13 works: `python -m venv .venv`, then the same lines.

## What green looks like

pytest needs no key and calls no model. It prints rows of dots and ends with one line, `N passed, 1 skipped`. The skip is pgvector, which needs Docker.

`requirements.txt` is exported from `uv.lock`, so pip and uv install the same versions.

## The first lab

Open this folder in VS Code and pick the `.venv` interpreter. Then:

```
python labs/lab_s2_env/part_1/setup_clone.py
```

It prints your Python version, checks the repo files, runs the full suite and ends with `pytest_exit 0`. The same lab as a notebook: `notebooks/section_02_set_up_any_provider_and_local/part_1_setup_clone.py`.

## Optional: pgvector

```
docker compose up -d
```

Install the driver with `uv sync --extra pgvector`, or with pip: `pip install "psycopg[binary]==3.3.4"`. Then run `labs/lab_s3_naive/part_3/compare_stores.py`.

## Optional: extras

```
uv sync --extra local-rerank
uv sync --extra docling
```

With pip: `pip install "sentence-transformers==3.4.1"` (local cross-encoder) or `pip install "docling==2.31.0"`.

## Optional: a model that writes the answers

Retrieval never needs one. To add generate, open `.env` and fill in one door: local Ollama (the default, no key: `ollama pull qwen3:8b`), Anthropic, or any OpenAI-compatible provider. The blocks are ready in `.env.example`, and README.md explains the three doors. Never commit `.env`.
