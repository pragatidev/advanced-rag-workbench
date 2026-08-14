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

Then pick a door. Details are in the README.

1. **Walk the pipeline (how lectures film):** `python labs/02_naive_pipeline.py` then open `store/naive/manifest.json`. Or open the file in VS Code and Run Cell on each `# %%` block. Notebook twin: `notebooks/02_naive_pipeline.ipynb`.
2. **Product (how a real app works):** `python -m ragbench serve` then open http://127.0.0.1:8787/ or `python examples/ticket_desk.py`
3. **Harness:** open this folder in VS Code. Ask Claude Code, Grok, or Cursor about TS-999. The `ask-acme` skill retrieves first. No key.
4. **CLI:** `python -m ragbench ask "What does error code TS-999 mean?" --pipeline hybrid`

**API (production generate only):** copy `.env.example` to `.env`, set URL + model + key, then `--generate api`. Never commit `.env`. Retrieve is still local.
