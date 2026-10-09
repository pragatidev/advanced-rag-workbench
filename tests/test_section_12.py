import json
import os
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
PART_2 = LAB_S12_GRAPH / "part_2" / "community_summaries.py"
SUMMARIES_JSON = LAB_S12_GRAPH / "part_2" / "community_summaries.json"


def _load(name: str, path: Path):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _part_1_module():
    return _load("s12_3_build_tiny_graph", PART_1)


def _part_2_module():
    return _load("s12_4_community_summaries", PART_2)


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


def test_s12_4_part_2_picks_up_part_1_and_never_the_hardcoded_summaries():
    """VO: 'We are not rebuilding the graph with new code, we are picking up the
    exact graph you watched get built.' And the seeded dictionary summaries in
    rag.graph.tiny are exactly what this lecture is NOT allowed to use."""
    source = PART_2.read_text(encoding="utf-8")
    assert "from build_tiny_graph import" in source
    assert "rag.graph.tiny" not in source
    for name in ("load_chunks", "build_members", "build_edges", "build_communities"):
        assert name in source


def test_s12_4_community_chunks_is_the_union_of_its_entities_chunk_lists():
    """VO: 'the community's evidence is just the union of those chunk id lists.'"""
    module = _part_2_module()
    p1 = _part_1_module()
    members = p1.build_members(p1.load_chunks())
    assert module.community_chunks(["TS-999", "billing", "national id", "revenue"], members) == [
        "error_catalog:fixed:0",
        "error_catalog:fixed:1",
        "faq:fixed:0",
        "filing_q2_2023:fixed:1",
        "privacy:fixed:0",
    ]
    assert module.community_chunks(["audit", "tenant"], members) == ["access_control:fixed:0"]


def test_s12_4_the_summary_is_derived_from_the_communitys_own_text():
    """VO: 'Never return a hand written string.' Every sentence of every summary
    has to be findable in the chunks that community owns."""
    module = _part_2_module()
    p1 = _part_1_module()
    chunks = p1.load_chunks()
    by_id = {c.chunk_id: c.text for c in chunks}
    members = p1.build_members(chunks)
    communities = p1.build_communities(members, p1.build_edges(chunks, members))
    for names in communities:
        texts = [by_id[cid] for cid in module.community_chunks(names, members)]
        blob = " ".join(texts)
        summary = module._extractive(names, texts)
        for sentence in summary.split(". "):
            assert sentence.rstrip(".").strip() in blob


def test_s12_4_the_run_prints_exactly_what_the_lecture_screens():
    """The shipped lane: .env.example ships RAGBENCH_GENERATE=extractive, so the
    student's screen reads mode extractive and model_calls 0."""
    env = dict(os.environ)
    env["RAGBENCH_GENERATE"] = "extractive"
    out = subprocess.run(
        [sys.executable, str(PART_2)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    ).stdout
    assert "community_0  entities: TS-999, billing, national id, revenue" in out
    assert (
        "  chunks: error_catalog:fixed:0, error_catalog:fixed:1, faq:fixed:0, "
        "filing_q2_2023:fixed:1, privacy:fixed:0" in out
    )
    assert "  summary: TS-999 is not retryable. Duplicate invoice failures are TS-999." in out
    assert "community_1  entities: audit, tenant" in out
    assert "  chunks: access_control:fixed:0" in out
    assert (
        "  summary: Shared runbooks are tagged tenant=shared. "
        "Privileged actions write an audit row." in out
    )
    assert "summaries_written 2   model_calls 0   mode extractive" in out
    # VO: 'the number of summaries is the number of communities'.
    assert out.count("entities: ") == 2


def test_s12_4_the_json_on_disk_is_the_global_index_part_4_reads():
    """VO: 'That file is the global index now.' Three keys per community."""
    env = dict(os.environ)
    env["RAGBENCH_GENERATE"] = "extractive"
    SUMMARIES_JSON.unlink(missing_ok=True)
    subprocess.run(
        [sys.executable, str(PART_2)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    written = json.loads(SUMMARIES_JSON.read_text(encoding="utf-8"))
    assert list(written) == ["community_0", "community_1"]
    for entry in written.values():
        assert set(entry) == {"entities", "chunks", "summary"}
        assert entry["summary"].strip()
    assert written["community_0"]["entities"] == [
        "TS-999", "billing", "national id", "revenue"
    ]
    assert written["community_1"]["chunks"] == ["access_control:fixed:0"]


PART_3 = LAB_S12_GRAPH / "part_3" / "global_vs_vector.py"


def _part_3_module():
    return _load("s12_5_global_vs_vector", PART_3)


def test_s12_5_the_path_block_is_lines_14_through_32():
    """SCREEN cue: 'highlight the sys.path block, lines 14 to 32.' Everything the
    VO reads off that block, in the order it reads it."""
    lines = PART_3.read_text(encoding="utf-8").splitlines()
    assert lines[13] == "import sys"
    assert lines[14] == "from pathlib import Path"
    # VO: 'Repo root three folders up so the rag package imports.'
    assert lines[17].startswith("ROOT = HERE.parents[2]")
    # VO: 'then part one and part two on the path by folder,
    #      because labs is not a Python package.'
    assert lines[20].startswith("# labs/ is not a package")
    assert lines[21] == 'for folder in ("part_1", "part_2"):'
    # VO: 'build_members, build_edges and build_communities come from part one.'
    assert lines[26] == "from build_tiny_graph import (  # noqa: E402"
    # VO: 'community_chunks and the extractive summarizer come from part two.'
    assert lines[31].startswith("from community_summaries import _extractive, community_chunks")


def test_s12_5_nothing_on_screen_is_a_second_copy_of_the_graph():
    """VO: 'I am not rewriting the graph here. If the graph on this screen
    disagrees with the one you built in part one, that is a bug, not a lesson.'"""
    source = PART_3.read_text(encoding="utf-8")
    for name in ("build_members", "build_edges", "build_communities"):
        assert f"def {name}" not in source
    assert "def _extractive" not in source
    assert "SEED = {" not in source
    assert "rag.graph.tiny" not in source


def test_s12_5_the_three_constants_the_vo_holds_on_screen():
    module = _part_3_module()
    assert module.QUESTION == "What are the main themes in this ACME corpus?"
    # SCREEN: 'THEME_TERMS and grade, verbatim.' VO: 'Four themes, and a short list of
    # words per theme written down before the run.'
    assert module.THEME_TERMS == {
        "sequential revenue reporting": ("sequential", "revenue", "quarter"),
        "billing integrity": ("billing", "invoice", "ts-999"),
        "least-privilege access": (
            "least privilege", "least-privilege", "privileged", "tenant", "audit"
        ),
        "PII minimization": ("pii", "national id", "redact", "retention"),
    }
    # VO: 'Themes across this corpus, with a colon. It is the whole lecture.'
    assert module.HAND_WRITTEN == "Themes across this corpus:"
    corpus = "\n".join(d.text for d in load_documents())
    assert corpus.count(module.HAND_WRITTEN) == 1


def test_s12_5_the_hand_written_sentence_is_the_only_thing_block_2_changes():
    """VO: 'It prints how many words it deleted. Nothing else changes.' And the
    cut is in memory only: the student's privacy.md is never edited on disk."""
    module = _part_3_module()
    before = {d.doc_id: d.text for d in load_documents()}
    docs = module.cut_hand_written(load_documents())
    changed = [d.doc_id for d in docs if d.text != before[d.doc_id]]
    assert changed == ["privacy"]
    cut = next(d for d in docs if d.doc_id == "privacy")
    assert module.HAND_WRITTEN not in cut.text
    # VO: 'Twenty nine words.'
    assert len(before["privacy"].split()) - len(cut.text.split()) == 29
    assert module.HAND_WRITTEN in (
        ROOT / "data" / "acme" / "policies" / "privacy.md"
    ).read_text(encoding="utf-8")


def test_s12_5_global_mode_never_takes_a_question():
    """VO: 'communities read, three; chunks searched at question time, zero. The
    reading was done at index time.' Global mode is handed the corpus, never the
    question, and never calls search."""
    import inspect

    module = _part_3_module()
    sig = inspect.signature(module.read_summaries)
    assert list(sig.parameters) == ["docs"]
    body = inspect.getsource(module.read_summaries)
    assert "QUESTION" not in body
    assert "search(" not in body


def test_s12_5_the_run_prints_exactly_what_the_lecture_screens():
    """Every line of all three blocks the VO reads off the terminal, pinned.

    The expected text is the capture block of the signed S12.5 script (2026-09-18),
    verbatim: one grader, four of four, one of four, three of four."""
    expected = "\n".join(
        [
            'QUESTION What are the main themes in this ACME corpus?',
            '',
            'BLOCK 1  vector search, corpus exactly as it ships',
            '  collection s12_5_shipped   chunks indexed 10',
            '  filing_q2_2023:fixed:1   0.3313',
            '  privacy:fixed:0          0.3156   <- carries the hand written themes sentence',
            '  figure_seats:fixed:0     0.2673',
            '    sequential revenue reporting   COVERED  sequential',
            '    billing integrity              COVERED  billing',
            '    least-privilege access         COVERED  least-privilege',
            '    PII minimization               COVERED  pii',
            '  themes covered 4 of 4',
            '',
            'BLOCK 2  the same search, with that one sentence deleted',
            '  removed 29 words from data/acme/policies/privacy.md in memory',
            '  data/acme/policies/privacy.md on disk still 86 words, not edited',
            '  collection s12_5_cut   chunks indexed 9',
            '  filing_q2_2023:fixed:1   0.3313',
            '  figure_seats:fixed:0     0.2673',
            '  filing_q2_2023:fixed:0   0.2572',
            '    sequential revenue reporting   COVERED  sequential',
            '    billing integrity              MISSING',
            '    least-privilege access         MISSING',
            '    PII minimization               MISSING',
            '  themes covered 1 of 4',
            '',
            'BLOCK 3  global mode on the same cut corpus, reading summaries',
            '  community_0  entities: TS-999, billing, national id',
            '    summary: TS-999 is not retryable. Duplicate invoice failures are TS-999.',
            '  community_1  entities: revenue',
            '    summary: Prior quarter revenue was 314 million USD. preface continues with ordinary language about risks, uncertainties, competitors, currency, and the possibility that actual results will differ.',
            '  community_2  entities: audit, tenant',
            '    summary: Shared runbooks are tagged tenant=shared. Privileged actions write an audit row.',
            '  communities read 3   chunks searched at question time 0',
            '  llm_extract_calls 0   seed dictionary, not a model extract',
            '    sequential revenue reporting   COVERED  revenue',
            '    billing integrity              COVERED  invoice',
            '    least-privilege access         COVERED  privileged',
            '    PII minimization               MISSING',
            '  themes covered 3 of 4',
        ]
    )
    out = subprocess.run(
        [sys.executable, str(PART_3)], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    assert out.rstrip("\n") == expected
    # VO: 'Filing chunk one is sitting at exactly the same 0.3313.'
    assert out.count("  filing_q2_2023:fixed:1   0.3313") == 2
    # VO: 'Privacy is gone from the list entirely.'
    assert out.count("privacy:fixed:0") == 1
    # No key, no network: the file imports nothing that reaches a provider.
    source = PART_3.read_text(encoding="utf-8")
    assert "rag.llm" not in source and "rag.embed " not in source


def test_s12_5_deleting_the_sentence_deletes_the_billing_revenue_link():
    """VO: 'three communities here, two in part two. That paragraph was the only
    place billing and revenue appeared together.'"""
    module = _part_3_module()
    p1 = _part_1_module()

    shipped_chunks = p1.load_chunks()
    shipped_members = p1.build_members(shipped_chunks)
    shipped_edges = p1.build_edges(shipped_chunks, shipped_members)
    assert shipped_edges[("billing", "revenue")] == 1
    assert len(p1.build_communities(shipped_members, shipped_edges)) == 2

    cut_chunks = []
    for doc in module.cut_hand_written(load_documents()):
        cut_chunks.extend(module.fixed_size(doc, size=80, overlap=0))
    cut_members = p1.build_members(cut_chunks)
    cut_edges = p1.build_edges(cut_chunks, cut_members)
    assert ("billing", "revenue") not in cut_edges
    assert p1.build_communities(cut_members, cut_edges) == [
        ["TS-999", "billing", "national id"],
        ["revenue"],
        ["audit", "tenant"],
    ]


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


# --- S12.6 pins: lab part 4, the refuse rule and the index bill --------------

PART_4 = LAB_S12_GRAPH / "part_4" / "run_graph.py"
GRAPH_BOARD = ROOT / "runs" / "smoke" / "graph_board.json"


def _part_4_module():
    return _load("s12_6_run_graph", PART_4)


def test_s12_6_part_4_reuses_parts_1_and_2_and_never_reimplements_the_graph():
    """VO: 'We are not rewriting the graph in this file.'"""
    source = PART_4.read_text(encoding="utf-8")
    assert "from build_tiny_graph import" in source
    assert "from community_summaries import community_chunks, summarize" in source
    assert "from rag.pipelines.hybrid import run_hybrid" in source
    # Nothing here is a second copy of part 1's graph logic.
    for owned in ("def build_members", "def build_edges", "def build_communities"):
        assert owned not in source
    # Free to run: the card ships extractive and never reaches a provider itself.
    assert 'os.environ.setdefault("RAGBENCH_GENERATE", "extractive")' in source
    assert "rag.llm" not in source


def test_s12_6_the_refuse_rule_really_is_four_lines():
    """VO: 'Here is the refuse rule, and it really is four lines.'"""
    import inspect

    module = _part_4_module()
    body = inspect.getsource(module.refuse_if_local_holds).splitlines()
    code = [line for line in body if line.strip() and not line.strip().startswith('"""')]
    assert len(code) == 4
    assert module.refuse_if_local_holds(True) == (
        "REFUSE: local questions still hold. Do not pay for a graph index."
    )
    assert module.refuse_if_local_holds(False) is None


def test_s12_6_the_failure_log_is_questions_that_failed_one_of_each_kind():
    """VO: 'Not questions somebody imagined. Questions that failed.'"""
    module = _part_4_module()
    assert module.FAILURE_LOG == (
        ("What does error code TS-999 mean?", "local"),
        ("What are the main themes in this ACME corpus?", "global"),
    )
    assert module.LOCAL_Q == module.FAILURE_LOG[0][0]
    # The global entry is the one that failed on screen in S12.5.
    assert module.GLOBAL_Q == "What are the main themes in this ACME corpus?"
    assert module.ANSWER_TOKEN == "TS-999"
    assert module.gate() is True


def test_s12_6_the_real_index_line_is_arithmetic_over_this_corpus():
    """VO: 'That number is not a claim I am making. It is arithmetic.'"""
    module = _part_4_module()
    chunks, _members, communities, _summaries, calls, mode = module.build_index()
    assert len(chunks) == 10
    assert len(communities) == 2
    assert calls == 0 and mode == "extractive"
    assert len(chunks) + len(communities) == 12


def test_s12_6_the_run_prints_exactly_what_the_lecture_screens():
    """Every line of all four blocks the VO reads off the terminal, pinned."""
    out = subprocess.run(
        [sys.executable, str(PART_4)], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout

    # BLOCK 1: local still holds, so the rule refuses out loud.
    assert out.startswith("BLOCK 1  the refuse gate\n")
    assert "  top hit error_catalog:rec:2:ctx  0.3333" in out
    assert "  TS-999 in retrieved text True" in out
    assert (
        "  REFUSE: local questions still hold. Do not pay for a graph index." in out
    )

    # BLOCK 2: the log, one line per question, with its kind.
    assert "  local   What does error code TS-999 mean?" in out
    assert "  global  What are the main themes in this ACME corpus?" in out
    assert "  a global question is in the log True" in out

    # BLOCK 3: the bill, toy number and real number side by side.
    assert "  chunks_indexed     10" in out
    assert "  entities           6" in out
    assert "  communities        2" in out
    assert "  llm_extract_calls  0   seed dictionary, not a model extract" in out
    assert "  llm_summary_calls  0   mode extractive" in out
    assert (
        "  a real GraphRAG index here: 10 extract calls + 2 summary calls = "
        "12 model calls before anyone asks a question" in out
    )

    # BLOCK 4: global mode reads summaries, it does not search.
    assert "  chunks searched at question time 0" in out
    assert "  community_0  entities: TS-999, billing, national id, revenue" in out
    assert "    TS-999 is not retryable. Duplicate invoice failures are TS-999." in out
    assert "  community_1  entities: audit, tenant" in out
    assert (
        "    Shared runbooks are tagged tenant=shared. "
        "Privileged actions write an audit row." in out
    )
    assert out.rstrip().endswith("graph_board.json")


def test_s12_6_the_board_file_is_the_receipt_for_the_section():
    """VO: 'That is your receipt for this section.'"""
    subprocess.run(
        [sys.executable, str(PART_4)], cwd=ROOT, capture_output=True, text=True, check=True
    )
    board = json.loads(GRAPH_BOARD.read_text(encoding="utf-8"))
    assert board == {
        "llm_extract_calls": 0,
        "llm_summary_calls": 0,
        "real_graphrag_index_calls": 12,
        "refuse_local": (
            "REFUSE: local questions still hold. Do not pay for a graph index."
        ),
    }
