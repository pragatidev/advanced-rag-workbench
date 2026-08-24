import subprocess
import sys
from pathlib import Path

from rag.ask import run_ask
from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.graph.tiny import answer_global, build, community_summaries, refuse_if_local_holds
from rag.settings import PROFILES

ROOT = Path(__file__).resolve().parents[1]
S12_1 = ROOT / "notebooks" / "section_12_graph_rag_and_when_to_refuse" / "S12_1_local_vs_global.py"


def test_section_12_graph_and_refuse():
    g = build()
    assert set(community_summaries()) >= {"revenue", "billing", "access", "privacy"}
    assert "sequential revenue" in answer_global("themes")["answer"].lower()
    assert refuse_if_local_holds(True)
    assert refuse_if_local_holds(False) is None
    assert g["index_cost"]["llm_extract_calls"] == 0


# --- S12.1 pins: every number the concept lecture says out loud -------------


def test_s12_1_the_corpus_is_ten_strips_and_naive_takes_three():
    """VO: 'the whole corpus is ten strips and the pipeline takes three'."""
    chunks = chunk_corpus(load_documents(), "fixed", size=80, overlap=0)
    assert len(chunks) == 10
    assert PROFILES["naive"]["k"] == 3
    assert PROFILES["naive"]["chunk_kwargs"]["size"] == 80


def test_s12_1_the_eighty_word_cut_splits_the_ts_999_paragraph():
    """VO: 'Strip zero ends at the merchant. Strip one starts at account, and
    carries the runbook owner and the lookup key sentence.'"""
    chunks = {c.chunk_id: c.text for c in chunk_corpus(load_documents(), "fixed", size=80, overlap=0)}
    strip_0 = chunks["error_catalog:fixed:0"]
    strip_1 = chunks["error_catalog:fixed:1"]
    assert strip_0.endswith("the merchant")
    assert strip_1.startswith("account.")
    assert "The runbook owner is billing-ops." in strip_1
    assert "The exact token TS-999 is the lookup key." in strip_1
    # The definition sentence and the lookup key sentence land on different strips.
    assert "TS-999 means the billing ledger rejected a duplicate invoice id." in strip_0
    assert "TS-999" not in strip_1.split("The exact token")[0]


def test_s12_1_the_natural_wording_misses_the_error_catalog_entirely():
    """VO: 'Three hits, and not one of them comes from the error catalog.'"""
    payload = run_ask(
        "What does error code TS-999 mean?", pipeline="naive", generate="extractive"
    )
    ids = [h["chunk_id"] for h in payload["hits"]]
    assert ids == ["privacy:fixed:1", "filing_q2_2023:fixed:1", "access_control:fixed:0"]
    assert not any(i.startswith("error_catalog") for i in ids)
    assert [round(h["score"], 4) for h in payload["hits"]] == [0.0245, -0.1218, -0.1319]
    # VO: 'The answer it printed is a fragment of a privacy file.'
    assert payload["answer"] == "vector hit will not list them."


def test_s12_1_the_bare_token_brings_the_home_strip_back_at_rank_two():
    """VO: 'the home strip comes back at rank two, score zero point zero seven four'."""
    payload = run_ask("TS-999", pipeline="naive", generate="extractive")
    hits = payload["hits"]
    assert hits[1]["chunk_id"] == "error_catalog:fixed:0"
    assert round(hits[1]["score"], 4) == 0.0742


def test_s12_1_the_screened_receipt_is_what_the_file_really_prints():
    """The two receipts on screen come from this file, run from the repo root."""
    out = subprocess.run(
        [sys.executable, str(S12_1)], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    assert 'run_ask("What does error code TS-999 mean?", pipeline="naive", generate="extractive")' in out
    assert "  privacy:fixed:1          0.0245" in out
    assert "  filing_q2_2023:fixed:1  -0.1218" in out
    assert "  access_control:fixed:0  -0.1319" in out
    assert "answer: vector hit will not list them." in out
    assert "  error_catalog:fixed:0    0.0742" in out
