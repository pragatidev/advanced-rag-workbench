"""STARTER Carry the entity into hop 2, then compose. Fill the TODOs. part_2 is the worked slice."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.ask import run_ask
from rag.settings import PROFILES, load_env
from rag.text import split_sentences, tokenize

load_env()

QUESTION = (
    "Can I paste a national id into ACME's assistant, and what does the "
    "retention policy require before that text reaches a model?"
)
ENTITY = "ACME"
HOP_1 = "Can I paste a national id into ACME's assistant"
HOP_2_NAIVE = "What does the retention policy require before that text reaches a model?"
HOP_2_REPAIRED = (
    "ACME's privacy and retention policy: what has to happen to a national id "
    "before a chunk reaches a model?"
)

STOPWORDS = frozenset(
    "a an and are as at be before but by can do does for from has have how i if in "
    "into is it its may must my no not of on or over s that the their them then "
    "there these this to was what when where which who will with you your".split()
)


def carries(sub_question: str, entity: str) -> bool:
    """The five second eye test, written down. Case insensitive substring."""
    # TODO: one line. Is the entity inside this sub question, ignoring case?
    raise NotImplementedError


def carry_forward(sub_question: str, entity: str, repaired: str) -> str:
    """Pass a sub question through untouched, or swap in the repair. Show the swap."""
    # TODO: return sub_question unchanged when it already carries the entity,
    # otherwise print before and after and return repaired
    raise NotImplementedError


def show(label: str, query: str, hits: list[dict]) -> None:
    print(label)
    print("  query:", query)
    print("  entity_carried:", carries(query, ENTITY))
    for hit in hits:
        print("   ", hit["doc_id"], round(hit["score"], 3))


def _content(text: str) -> list[str]:
    return [word for word in tokenize(text) if word not in STOPWORDS]


def _answering_sentence(sub_question: str, chunk_text: str) -> str:
    """The sentence in this chunk most made of the words the sub question asked about.

    Two sentences are skipped. A question is not an answer. And a sentence that
    starts with '#' is a markdown title the fixed size chunker glued onto the
    text that followed it, so it is a heading, not a claim.
    """
    wanted = set(_content(sub_question))
    best, best_score = "", -1.0
    for sentence in split_sentences(chunk_text):
        if sentence.endswith("?") or sentence.lstrip().startswith("#"):
            continue
        words = _content(sentence)
        if not words:
            continue
        score = len(wanted.intersection(words)) / len(words)
        if score > best_score:
            best, best_score = sentence, score
    return best


def compose(hop1_hits: list[dict], hop2_hits: list[dict]) -> str:
    """One answer from the TOP hit of each hop. Not a merged, resorted pile.

    Each hop owns one clause of the question, so each contributes one sentence
    and one citation. Extractive and deterministic. No model call.
    """
    # TODO: take the top hit of EACH hop, pull the answering sentence out of each,
    # and return one string citing both chunk ids in brackets, hop 1 then hop 2
    raise NotImplementedError


print("k =", PROFILES["naive"]["k"])

hop_1_hits = run_ask(HOP_1, pipeline="naive", generate="extractive")["hits"]
show("HOP 1", HOP_1, hop_1_hits)

hop_2_query = carry_forward(HOP_2_NAIVE, ENTITY, HOP_2_REPAIRED)
hop_2_hits = run_ask(hop_2_query, pipeline="naive", generate="extractive")["hits"]
show("HOP 2 (repaired)", hop_2_query, hop_2_hits)

print("chunks_retrieved", len(hop_1_hits) + len(hop_2_hits))
print("chunks_used", 2)
print("composed_from", hop_1_hits[0]["chunk_id"], "+", hop_2_hits[0]["chunk_id"])
print("ANSWER:", compose(hop_1_hits, hop_2_hits))
