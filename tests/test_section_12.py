import subprocess
import sys
from pathlib import Path

from rag.ask import run_ask
from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.graph.tiny import answer_global, build, community_summaries, refuse_if_local_holds
from rag.settings import PROFILES

ROOT = Path(__file__).resolve().parents[1]
S12_DIR = ROOT / "notebooks" / "section_12_graph_rag_and_when_to_refuse"
S12_1 = S12_DIR / "S12_1_local_vs_global.py"
S12_1_REWORDED = S12_DIR / "S12_1_global_reworded.py"

LOCAL_ANSWER = "TS-999 means the billing ledger rejected a duplicate invoice id."
GLOBAL_ANSWER = (
    "sequential revenue reporting, billing integrity, "
    "least-privilege access, and PII minimization"
)


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


def test_s12_1_the_corpus_is_the_seven_acme_source_files():
    """VO: 'Here are two questions you could ask the same seven files.'"""
    names = sorted(d.doc_id for d in load_documents())
    assert len(names) == 7


def test_s12_1_the_eighty_word_cut_splits_the_ts_999_paragraph():
    """Corpus-stability pin: the fixed 80-word cut is what makes the local miss
    reproducible, so the two receipts below stay the same on every machine."""
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


def test_s12_1_the_documents_own_words_bring_the_error_catalog_to_rank_one():
    """VO: 'There it is. Error catalog at rank one, and the sentence came back. True.'"""
    payload = run_ask(
        "TS-999 billing ledger duplicate invoice id", pipeline="naive", generate="extractive"
    )
    ids = [h["chunk_id"] for h in payload["hits"]]
    assert ids == ["error_catalog:fixed:0", "faq:fixed:0", "q2_kpis:fixed:0"]
    assert [round(h["score"], 4) for h in payload["hits"]] == [0.3098, 0.2500, 0.1270]
    assert any(LOCAL_ANSWER.lower() in h["text"].lower() for h in payload["hits"])


def test_s12_1_the_global_question_tops_out_on_a_figure_caption():
    """VO: 'The top hit is a figure caption about seats by region.
    East four thousand one hundred, West three thousand nine hundred.'"""
    payload = run_ask("What themes run across all of this?", pipeline="naive", generate="extractive")
    ids = [h["chunk_id"] for h in payload["hits"]]
    assert ids == ["figure_seats:fixed:0", "privacy:fixed:1", "filing_q2_2023:fixed:1"]
    assert [round(h["score"], 4) for h in payload["hits"]] == [0.2521, 0.1939, 0.1607]
    top = payload["hits"][0]["text"]
    assert "seats by region" in top and "East 4100" in top and "West 3900" in top
    # The four-theme sentence is NOT in what came back.
    assert not any(GLOBAL_ANSWER.lower() in h["text"].lower() for h in payload["hits"])


def test_s12_1_the_reworded_global_only_works_because_a_human_pre_wrote_it():
    """VO: 'It worked because somebody sat down and wrote this sentence into the
    privacy policy by hand.' The green is real, and the reason is the lecture."""
    payload = run_ask(
        "What are the themes across this corpus?", pipeline="naive", generate="extractive"
    )
    assert payload["answer"] == (
        "Sequential revenue reporting, billing integrity, "
        "least-privilege access, and PII minimization."
    )
    # The answer is a verbatim span of one hand-written chunk, not a synthesis.
    privacy = (ROOT / "data" / "acme" / "policies" / "privacy.md").read_text(encoding="utf-8")
    assert "Themes across this corpus: " + GLOBAL_ANSWER + "." in privacy


def test_s12_1_the_screened_receipts_are_what_the_files_really_print():
    """Every line held on screen comes from these two files, run from the repo root."""
    three = subprocess.run(
        [sys.executable, str(S12_1)], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    assert 'run_ask("What does error code TS-999 mean?", pipeline="naive")' in three
    assert "  privacy:fixed:1            0.0245" in three
    assert "  filing_q2_2023:fixed:1    -0.1218" in three
    assert "  access_control:fixed:0    -0.1319" in three
    assert three.count("answer sentence in the returned strips: False") == 1
    assert "  error_catalog:fixed:0      0.3098" in three
    assert three.count("answer sentence in the returned strips: True") == 1
    assert "  figure_seats:fixed:0       0.2521" in three
    assert "four-theme sentence in the returned strips: False" in three

    fourth = subprocess.run(
        [sys.executable, str(S12_1_REWORDED)], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    assert 'run_ask("What are the themes across this corpus?", pipeline="naive")' in fourth
    assert "  filing_q2_2023:fixed:0     0.3780" in fourth
    assert "  figure_seats:fixed:0       0.3509" in fourth
    assert "  privacy:fixed:0            0.3272" in fourth
    assert (
        "answer: Sequential revenue reporting, billing integrity, "
        "least-privilege access, and PII minimization." in fourth
    )
