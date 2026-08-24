"""STARTER Hop 2 drops the entity. Fill the TODOs. part_1 is the first working slice."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import the package symbols this lab needs
from rag.ask import run_ask
from rag.settings import PROFILES, load_env

load_env()

QUESTION = (
    "Can I paste a national id into ACME's assistant, and what does the "
    "retention policy require before that text reaches a model?"
)


def naive_split(question: str) -> tuple[str, str]:
    """Split once on ', and '. The leftover clause becomes its own search."""
    # TODO: return the first half as typed, and the second half capitalised
    raise NotImplementedError


clause_1, clause_2 = naive_split(QUESTION)


def show(label: str, query: str) -> dict:
    result = run_ask(query, pipeline="naive", generate="extractive")
    print(label)
    print("  query:", query)
    # TODO: print entity_carried, the one boolean this whole lab exists to show
    for hit in result["hits"]:
        print("   ", hit["doc_id"], round(hit["score"], 3))
    return result


print("k =", PROFILES["naive"]["k"])
show("HOP 1", clause_1)
show("HOP 2 (naive)", clause_2)
print("no exception raised. the run exited clean.")
