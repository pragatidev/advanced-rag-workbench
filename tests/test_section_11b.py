"""Pins for section 11B, the two-hop entity-drop lab.

Lecture S11B.3 reads a captured run on screen: the hop 2 query with ACME
missing from it, the entity_carried booleans, and both ranked hit lists. If any
of these drift, the output spliced into that script becomes a lie. So pin them.
"""

from pathlib import Path

from rag.ask import run_ask
from rag.settings import PROFILES

ROOT = Path(__file__).resolve().parents[1]
PART_1 = ROOT / "labs" / "lab_s11b_hop" / "part_1" / "naive_hop.py"

QUESTION = (
    "Can I paste a national id into ACME's assistant, and what does the "
    "retention policy require before that text reaches a model?"
)
CLAUSE_1 = "Can I paste a national id into ACME's assistant"
CLAUSE_2 = "What does the retention policy require before that text reaches a model?"


def _naive_split(question: str) -> tuple[str, str]:
    first, _, second = question.partition(", and ")
    return first, second[:1].upper() + second[1:]


def test_the_question_on_screen_is_the_one_the_concept_taught():
    # The literal is wrapped across two source lines; compare on collapsed text.
    source = " ".join(PART_1.read_text(encoding="utf-8").replace('"', " ").split())
    assert QUESTION in source
    assert QUESTION.count("ACME") == 1


def test_naive_split_drops_the_entity_from_hop_2():
    clause_1, clause_2 = _naive_split(QUESTION)
    assert clause_1 == CLAUSE_1
    assert clause_2 == CLAUSE_2
    assert "ACME" in clause_1.upper()
    assert "ACME" not in clause_2.upper()


def test_k_on_screen_is_read_from_the_profile():
    assert PROFILES["naive"]["k"] == 3


def test_hop_1_retrieves_the_policy_that_answers_it():
    hits = run_ask(CLAUSE_1, pipeline="naive", generate="extractive")["hits"]
    assert [h["doc_id"] for h in hits] == ["faq", "privacy", "access_control"]


def test_hop_2_returns_a_full_wrong_list_and_never_the_retention_doc():
    hits = run_ask(CLAUSE_2, pipeline="naive", generate="extractive")["hits"]
    doc_ids = [h["doc_id"] for h in hits]
    # Not empty, not an error: three confident rows. That is what makes it expensive.
    assert doc_ids == ["q2_kpis", "error_catalog", "filing_q2_2023"]
    assert len(doc_ids) == PROFILES["naive"]["k"]
    # privacy.md is the document that actually carries the retention rule.
    assert "privacy" not in doc_ids


def test_privacy_doc_really_is_the_retention_answer_hop_2_missed():
    text = (ROOT / "data" / "acme" / "policies" / "privacy.md").read_text(encoding="utf-8")
    assert "retention" in text.lower()
    assert "redact national id before a chunk is sent to a model" in text


def test_privacy_is_the_only_document_carrying_the_retention_rule():
    # The lecture says on screen: "in this corpus, privacy.md is the ONLY document
    # that carries the retention rule". Drop a second retention doc into the corpus
    # and that sentence stops being true, so fail here instead of on camera.
    carriers = sorted(
        p.relative_to(ROOT).as_posix()
        for p in (ROOT / "data").rglob("*.md")
        if "retention" in p.read_text(encoding="utf-8").lower()
    )
    assert carriers == ["data/acme/policies/privacy.md"]


def test_solution_matches_the_walked_file():
    solution = ROOT / "labs" / "lab_s11b_hop" / "solution" / "naive_hop.py"
    assert solution.read_text(encoding="utf-8") == PART_1.read_text(encoding="utf-8")


# --- S11B.4: the repair and the composition -------------------------------
# Lecture S11B.4 reads a second captured run on screen: the repaired hop 2
# query with ACME inside it, entity_carried True, privacy on top, and one
# composed answer citing both hops. Pin every line of it.

PART_2 = ROOT / "labs" / "lab_s11b_hop" / "part_2" / "repaired_hop.py"

HOP_2_REPAIRED = (
    "ACME's privacy and retention policy: what has to happen to a national id "
    "before a chunk reaches a model?"
)


def _part_2():
    import importlib.util

    spec = importlib.util.spec_from_file_location("_s11b4_probe", PART_2)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_repaired_hop_2_carries_the_entity_and_the_naive_one_does_not():
    module = _part_2()
    assert module.carries(HOP_2_REPAIRED, "ACME") is True
    assert module.carries(CLAUSE_2, "ACME") is False
    # The broken query stays in the file next to its repair. That is the lesson.
    assert module.HOP_2_NAIVE == CLAUSE_2
    assert module.HOP_2_REPAIRED == HOP_2_REPAIRED


def test_carry_forward_swaps_only_when_the_entity_is_missing():
    module = _part_2()
    assert module.carry_forward(CLAUSE_1, "ACME", "REPAIR") == CLAUSE_1
    assert module.carry_forward(CLAUSE_2, "ACME", "REPAIR") == "REPAIR"


def test_the_repaired_hop_2_puts_the_retention_doc_on_top():
    hits = run_ask(HOP_2_REPAIRED, pipeline="naive", generate="extractive")["hits"]
    doc_ids = [h["doc_id"] for h in hits]
    # The naive hop 2 returned q2_kpis / error_catalog / filing_q2_2023 and never
    # privacy. One string changed and the search is pointed at the company again.
    assert doc_ids == ["privacy", "faq", "access_control"]
    assert doc_ids[0] == "privacy"


def test_composed_answer_is_built_from_the_top_hit_of_each_hop():
    module = _part_2()
    hop_1 = run_ask(CLAUSE_1, pipeline="naive", generate="extractive")["hits"]
    hop_2 = run_ask(HOP_2_REPAIRED, pipeline="naive", generate="extractive")["hits"]
    assert hop_1[0]["chunk_id"] == "faq:fixed:0"
    assert hop_2[0]["chunk_id"] == "privacy:fixed:0"
    answer = module.compose(hop_1, hop_2)
    assert answer == (
        "The assistant redacts that field. [faq:fixed:0] "
        "Retrieval must redact national id before a chunk is sent to a model. "
        "[privacy:fixed:0]"
    )
    # Both citations, in hop order.
    assert answer.index("[faq:fixed:0]") < answer.index("[privacy:fixed:0]")


def test_six_retrieved_two_used_is_true_and_not_a_slogan():
    hop_1 = run_ask(CLAUSE_1, pipeline="naive", generate="extractive")["hits"]
    hop_2 = run_ask(HOP_2_REPAIRED, pipeline="naive", generate="extractive")["hits"]
    assert len(hop_1) + len(hop_2) == 6
    # compose reads exactly one chunk per hop, never a merged and resorted pile.
    assert PART_2.read_text(encoding="utf-8").count("hop1_hits[0]") == 1
    assert PART_2.read_text(encoding="utf-8").count("hop2_hits[0]") == 1


def test_part_2_makes_no_model_call():
    source = PART_2.read_text(encoding="utf-8")
    for forbidden in ("rag.llm", "import chat", "openai", "requests"):
        assert forbidden not in source


def test_part_2_solution_matches_the_walked_file():
    solution = ROOT / "labs" / "lab_s11b_hop" / "solution" / "repaired_hop.py"
    assert solution.read_text(encoding="utf-8") == PART_2.read_text(encoding="utf-8")
