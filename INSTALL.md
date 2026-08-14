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

Then work like a normal Python project. Open this folder in VS Code.

1. **Walk (how you build RAG):** open `labs/02_naive_pipeline.py` and Run, or Run Cell on each `# %%` block. Then open `store/naive/manifest.json`. Notebook twin: `notebooks/02_naive_pipeline.ipynb`.
2. **Product (how it ships):** `python -m ragbench serve` then open http://127.0.0.1:8787/ or `python examples/ticket_desk.py`
3. **Harness:** same folder, ask Claude Code / Grok / Cursor about TS-999. It should run the lab or `run_ask`, not invent files.
4. **CLI (optional):** `python -m ragbench ask "What does error code TS-999 mean?" --pipeline hybrid`

**API (production generate only):** copy `.env.example` to `.env`, set URL + model + key, then `--generate api`. Never commit `.env`. Retrieve is still local.
