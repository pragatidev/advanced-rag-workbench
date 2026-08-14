"""The settings cell. Every named choice a notebook would print lives here."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORE_ROOT = ROOT / "store"

# Lab embedder. Not a hosted semantic model. Named on purpose so the screen walk
# can say what is running and what you would swap on Monday.
LAB_EMBEDDER = {
    "name": "ToyEmbedder",
    "dim": 64,
    "semantic_mode": True,
    "role": "lab stand-in",
    "why": (
        "Reproduces the TS-999 miss (rare IDs fade, 'error codes in general' ranks first) "
        "without downloading a 400MB model."
    ),
    "production_swap": [
        "OpenAI text-embedding-3-small",
        "Voyage voyage-3-lite",
        "sentence-transformers/all-MiniLM-L6-v2",
    ],
}

PROFILES = {
    "naive": {
        "chunker": "fixed",
        "chunk_kwargs": {"size": 80, "overlap": 0},
        "contextual": False,
        "search": "dense",
        "k": 3,
    },
    "hybrid": {
        "chunker": "recursive",
        "chunk_kwargs": {},
        "contextual": True,
        "search": "hybrid",
        "k": 4,
    },
}
