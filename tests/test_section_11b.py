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


def test_solution_matches_the_walked_file():
    solution = ROOT / "labs" / "lab_s11b_hop" / "solution" / "naive_hop.py"
    assert solution.read_text(encoding="utf-8") == PART_1.read_text(encoding="utf-8")
