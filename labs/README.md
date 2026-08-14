# Labs

Moved. Lecture walks now live under `notebooks/section_XX/`. Open those in VS Code and Run.

| File | Lecture | What you see |
|---|---|---|
| `02_naive_pipeline.py` | 2.2 | load → chunk → **named embedder** → **store/naive/** → retrieve → generate |
| `03_compare_chunkers.py` | 3.2 | fixed vs recursive vs semantic vs parent-child on the 3% sentence |
| `04_hybrid_vs_dense.py` | 4.2 | same TS-999 question, two stores |

Twin notebook for people who think in `.ipynb`: `notebooks/02_naive_pipeline.ipynb`. Same stages. Same store folder.

```
python labs/02_naive_pipeline.py
```

Then open `store/naive/manifest.json`. The embedder name is in that file.
