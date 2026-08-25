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


# --- S12.3 pins: the lab part 1 file and every number its run prints ---------

LAB_S12_GRAPH = ROOT / "labs" / "lab_s12_graph"
PART_1 = LAB_S12_GRAPH / "part_1" / "build_tiny_graph.py"
STARTER_1 = LAB_S12_GRAPH / "starter" / "build_tiny_graph.py"


def _part_1_module():
    import importlib.util

    spec = importlib.util.spec_from_file_location("s12_3_build_tiny_graph", PART_1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _part_1_chunks():
    return [c for d in load_documents() for c in __import__(
        "rag.chunkers", fromlist=["fixed_size"]
    ).fixed_size(d, size=80, overlap=0)]


def test_s12_3_the_import_block_really_is_lines_1_through_12():
    """SCREEN cue: 'Hold on the import block, lines 1 through 12.'"""
    lines = PART_1.read_text(encoding="utf-8").splitlines()
    assert lines[6].startswith("ROOT = Path(__file__).resolve().parents[3]")
    assert lines[7] == "if str(ROOT) not in sys.path:"
    assert lines[8] == "    sys.path.insert(0, str(ROOT))"
    # VO names load_documents first, then fixed_size. Screen order must agree.
    assert lines[10] == "from rag.corpus import load_documents"
    assert lines[11] == "from rag.chunkers import fixed_size"
    assert lines[12] == ""


def test_s12_3_every_seed_term_appears_verbatim_in_the_corpus():
    """VO: 'Every seed term is checked against the corpus before anything is built.'"""
    module = _part_1_module()
    module.assert_seeds_are_real(load_documents())  # must not raise
    assert len(module.SEED_TERMS) == 13
    for required in [
        "TS-999", "billing ledger", "duplicate invoice id", "billing-ops",
        "national id", "PII", "redact", "AC-2", "tenant", "shared passwords",
        "revenue", "prior quarter revenue", "seats by region",
    ]:
        assert required in module.SEED_TERMS


def test_s12_3_the_guard_rail_stops_and_names_the_term_that_matched_nothing():
    """VO: 'It stops and names the term that matched nothing.'"""
    import pytest

    module = _part_1_module()
    module.SEED_TERMS["typo entity"] = ["TS-9999 not in any file"]
    try:
        with pytest.raises(SystemExit) as caught:
            module.assert_seeds_are_real(load_documents())
        assert "typo entity" in str(caught.value)
        assert "TS-9999 not in any file" in str(caught.value)
    finally:
        del module.SEED_TERMS["typo entity"]


def test_s12_3_the_graph_the_lecture_holds_on_screen():
    """Every number the VO reads off the run, pinned."""
    module = _part_1_module()
    members = module.build_members(_part_1_chunks())
    edges = module.build_edges(members)
    communities = module.connected_components(sorted(members), edges)

    assert len(members) == 13
    assert len(edges) == 21
    assert {e: len(ids) for e, ids in members.items()} == {
        "AC-2": 1, "PII": 1, "TS-999": 3, "billing ledger": 1, "billing-ops": 2,
        "duplicate invoice id": 2, "national id": 2, "prior quarter revenue": 1,
        "redact": 2, "revenue": 2, "seats by region": 1, "shared passwords": 1,
        "tenant": 1,
    }
    assert communities == [
        ["AC-2", "shared passwords", "tenant"],
        [
            "PII", "TS-999", "billing ledger", "billing-ops",
            "duplicate invoice id", "national id", "prior quarter revenue",
            "redact", "revenue",
        ],
        ["seats by region"],
    ]
    assert module.docs_of(members, communities[0]) == ["access_control"]
    assert module.docs_of(members, communities[1]) == [
        "error_catalog", "faq", "filing_q2_2023", "privacy"
    ]
    assert module.docs_of(members, communities[2]) == ["figure_seats"]


def test_s12_3_the_big_community_is_glued_by_the_hand_written_themes_sentence():
    """Realizer fact for the writer: community_1 is one blob because privacy:fixed:0
    carries BOTH 'PII' and the pre-written 'sequential revenue reporting' sentence.
    A human did sort part of this graph. Pinned so the lecture cannot drift off it."""
    module = _part_1_module()
    members = module.build_members(_part_1_chunks())
    bridge = "privacy:fixed:0"
    on_bridge = sorted(e for e, ids in members.items() if bridge in ids)
    assert on_bridge == ["PII", "national id", "redact", "revenue"]
    text = {c.chunk_id: c.text for c in _part_1_chunks()}[bridge]
    assert "Themes across this corpus: sequential revenue reporting" in text


def test_s12_3_the_run_prints_exactly_what_the_lecture_screens():
    out = subprocess.run(
        [sys.executable, str(PART_1)], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    assert out.startswith(
        "CORPUS   7 documents, 10 chunks (fixed, size=80, overlap=0)\n"
    )
    assert "SEEDS    13 terms, hand written, not model extracted" in out
    assert "NODES    13" in out
    assert "  TS-999                 3 chunks" in out
    assert "EDGES    21 pairs share at least one chunk" in out
    assert "COMMUNITIES  3" in out
    assert "    entities: AC-2, shared passwords, tenant" in out
    assert "    docs:     error_catalog, faq, filing_q2_2023, privacy" in out
    assert out.rstrip().endswith("CLUSTERING   connected components, not Leiden")
    # No key, no network: the file imports nothing that reaches a provider.
    source = PART_1.read_text(encoding="utf-8")
    assert "rag.llm" not in source and "rag.embed" not in source


def test_s12_3_the_starter_withholds_the_three_build_functions_and_nothing_else():
    starter = STARTER_1.read_text(encoding="utf-8")
    assert starter.count("raise NotImplementedError") == 3
    for withheld in ["TODO 1", "TODO 2", "TODO 3"]:
        assert withheld in starter
    # The dict, the guard rail and the printing are given, so the student edits
    # only the graph logic.
    assert "def assert_seeds_are_real" in starter
    assert "SEED TERM NOT IN CORPUS" in starter
    assert "CLUSTERING   connected components, not Leiden" in starter
    run = subprocess.run(
        [sys.executable, str(STARTER_1)], cwd=ROOT, capture_output=True, text=True
    )
    assert run.returncode == 1
    assert "TODO 1: build the nodes and their members" in run.stderr
