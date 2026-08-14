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

Then pick a door. Both are in the README.

1. **Harness:** open this folder in VS Code. Ask Claude Code, Grok, or Cursor to run pytest or hybrid on TS-999. No key.
2. **CLI:** `python -m ragbench ask "What does error code TS-999 mean?" --pipeline hybrid`

**API (production generate only):** copy `.env.example` to `.env`, set URL + model + key, then `--generate api`. Never commit `.env`.
