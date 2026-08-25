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


def test_s12_3_the_import_block_is_lines_8_through_16():
    """SCREEN cue: 'highlight the import block, lines 8 through 18.'"""
    lines = PART_1.read_text(encoding="utf-8").splitlines()
    assert lines[7] == "import sys"
    assert lines[8] == "from pathlib import Path"
    assert lines[10].startswith("ROOT = Path(__file__).resolve().parents[3]")
    assert lines[11] == "if str(ROOT) not in sys.path:"
    assert lines[12] == "    sys.path.insert(0, str(ROOT))"
    # VO names load_documents and fixed_size as "the only two that matter".
    assert lines[14] == "from rag.chunkers import fixed_size"
    assert lines[15] == "from rag.corpus import load_documents"
    assert lines[17].startswith("# The fake extractor")


def test_s12_3_the_seed_dictionary_is_six_entries_that_all_live_in_the_corpus():
    """VO: 'six of them, chosen because they already live in the ACME corpus'."""
    module = _part_1_module()
    assert list(module.SEED) == [
        "TS-999", "billing", "national id", "revenue", "tenant", "audit"
    ]
    corpus = "\n".join(d.text for d in load_documents()).lower()
    for needles in module.SEED.values():
        for needle in needles:
            assert needle == needle.lower()
            assert needle in corpus


def test_s12_3_the_cut_is_the_same_ten_strips_the_naive_pipeline_uses():
    """VO: 'the same chunk ids you saw in the last lecture'."""
    module = _part_1_module()
    chunks = module.load_chunks()
    assert len(chunks) == 10
    assert [c.chunk_id for c in chunks] == [
        c.chunk_id for c in chunk_corpus(load_documents(), "fixed", size=80, overlap=0)
    ]


def test_s12_3_the_graph_the_lecture_holds_on_screen():
    """Every number the VO reads off the run, pinned."""
    module = _part_1_module()
    chunks = module.load_chunks()
    members = module.build_members(chunks)
    edges = module.build_edges(chunks, members)
    communities = module.build_communities(members, edges)

    assert members == {
        "TS-999": ["error_catalog:fixed:0", "error_catalog:fixed:1", "faq:fixed:0"],
        "billing": [
            "error_catalog:fixed:0", "error_catalog:fixed:1",
            "privacy:fixed:0", "faq:fixed:0",
        ],
        "national id": ["privacy:fixed:0", "faq:fixed:0"],
        "revenue": ["filing_q2_2023:fixed:1", "privacy:fixed:0"],
        "tenant": ["access_control:fixed:0"],
        "audit": ["access_control:fixed:0"],
    }
    assert dict(sorted(edges.items())) == {
        ("TS-999", "billing"): 3,
        ("TS-999", "national id"): 1,
        ("audit", "tenant"): 1,
        ("billing", "national id"): 2,
        ("billing", "revenue"): 1,
        ("national id", "revenue"): 1,
    }
    assert communities == [
        ["TS-999", "billing", "national id", "revenue"],
        ["audit", "tenant"],
    ]


def test_s12_3_ts_999_is_three_chunks_against_four_editor_matches():
    """VO: 'the editor tells you four... That number will never match the screen.'
    Four literal TS-999 matches inside error_catalog.md, landing on two chunk ids,
    plus one chunk in the FAQ, so the node reads three."""
    module = _part_1_module()
    members = module.build_members(module.load_chunks())
    catalog = (ROOT / "data" / "acme" / "runbooks" / "error_catalog.md").read_text(
        encoding="utf-8"
    )
    assert catalog.count("TS-999") == 4
    assert len(members["TS-999"]) == 3
    # VO: 'One of them is not the error catalog at all.'
    assert "faq:fixed:0" in members["TS-999"]
    faq = (ROOT / "data" / "acme" / "faq" / "support.md").read_text(encoding="utf-8")
    assert "Duplicate invoice failures are TS-999." in faq


def test_s12_3_revenue_and_billing_do_share_the_privacy_chunk():
    """REALIZER FACT, contradicts the r3 VO line 'revenue and billing never appear
    in the same chunk anywhere in this corpus'. They do: privacy:fixed:0 carries the
    hand-written themes sentence naming both. The EDGES block prints the direct link."""
    module = _part_1_module()
    chunks = module.load_chunks()
    members = module.build_members(chunks)
    shared = set(members["revenue"]) & set(members["billing"])
    assert shared == {"privacy:fixed:0"}
    bridge = {c.chunk_id: c.text for c in chunks}["privacy:fixed:0"]
    assert "Themes across this corpus: sequential revenue reporting, billing integrity" in bridge
    edges = module.build_edges(chunks, members)
    assert edges[("billing", "revenue")] == 1


def test_s12_3_the_run_prints_exactly_what_the_lecture_screens():
    out = subprocess.run(
        [sys.executable, str(PART_1)], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    assert out.startswith("chunks 10\n")
    assert "extracted_by seed_dict   llm_extract_calls 0" in out
    assert "  TS-999  chunks 3" in out
    assert "      faq:fixed:0" in out
    assert "  billing -- revenue   shared_chunks 1" in out
    assert "  community_0  members: TS-999, billing, national id, revenue" in out
    assert out.rstrip().endswith("community_1  members: audit, tenant")
    # No key, no network: the file imports nothing that reaches a provider.
    source = PART_1.read_text(encoding="utf-8")
    assert "rag.llm" not in source and "rag.embed" not in source


def test_s12_3_the_starter_withholds_the_three_build_functions_and_nothing_else():
    starter = STARTER_1.read_text(encoding="utf-8")
    assert starter.count("raise NotImplementedError") == 3
    for withheld in ["TODO 1", "TODO 2", "TODO 3"]:
        assert withheld in starter
    # The dict, the cut and the printing are given, so the student edits only
    # the graph logic.
    assert "SEED = {" in starter
    assert "def load_chunks" in starter
    assert 'print("extracted_by seed_dict   llm_extract_calls 0")' in starter
    run = subprocess.run(
        [sys.executable, str(STARTER_1)], cwd=ROOT, capture_output=True, text=True
    )
    assert run.returncode == 1
    assert "TODO 1: build the nodes and their members" in run.stderr
