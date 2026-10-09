import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks/section_18_optional_2026_frontier_cards/S18_1_plan_then_retrieve.py"
NB2 = ROOT / "notebooks/section_18_optional_2026_frontier_cards/S18_2_three_retrieval_tools.py"
NB3 = ROOT / "notebooks/section_18_optional_2026_frontier_cards/S18_3_conversation_memory.py"
NB4 = ROOT / "notebooks/section_18_optional_2026_frontier_cards/S18_4_ast_chunking.py"
NB5 = ROOT / "notebooks/section_18_optional_2026_frontier_cards/S18_5_hot_ram.py"


def test_section_18_1_plan_then_retrieve():
    page = (ROOT / "docs" / "mechanisms" / "plan_then_retrieve.md").read_text(encoding="utf-8")
    assert "Not the Monday loop" in page
    assert "Plan*RAG" in page
    assert "DAG outside the model context" in page
    assert "Two hops run in parallel" in page
    assert "Reason-in-Documents compressor" in page
    assert "verbose hit" in page
    assert "Plus 26.4 percent is their comparison" in page
    out = subprocess.run(
        [sys.executable, str(NB)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    ).stdout
    assert "=== not the Monday loop ===" in out
    assert "plan Plan*RAG DAG outside the window" in out
    assert "hops two parallel" in out
    assert "compressor Reason-in-Documents between verbose hit and next thought" in out
    assert "deeprag named +26.4 percent is their comparison" in out
    assert "rule A longer agent trace is not a plan." in out


def test_section_18_2_three_retrieval_tools():
    page = (ROOT / "docs" / "mechanisms" / "three_retrieval_tools.md").read_text(encoding="utf-8")
    assert "Not the Monday loop" in page
    assert "A-RAG" in page
    assert "Keyword search" in page
    assert "Semantic search" in page
    assert "Chunk-read" in page
    assert "The agent picks the granularity" in page
    out = subprocess.run(
        [sys.executable, str(NB2)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    ).stdout
    assert "=== not one top k ===" in out
    assert "file docs/mechanisms/three_retrieval_tools.md" in out
    assert "tools keyword, dense, chunk-read" in out
    assert "agent picks granularity" in out
    assert "rule Retrieve is not always one top-k." in out


def test_section_18_3_conversation_memory():
    page = (ROOT / "docs" / "mechanisms" / "conversation_memory.md").read_text(encoding="utf-8")
    assert "Not the Monday loop" in page
    assert "The vector store is memory" in page
    assert "Priya's team is Helix-East, updated 12 Mar" in page
    assert "right drawer first, then the left" in page
    assert "Mem0" in page
    assert "Zep and Graphiti" in page
    assert "Mixing them is how last week's refund policy becomes today's" in page
    out = subprocess.run(
        [sys.executable, str(NB3)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    ).stdout
    assert "=== not the document index ===" in out
    assert "file docs/mechanisms/conversation_memory.md" in out
    assert "left ACME policies" in out
    assert "right Priya's team is Helix-East, updated 12 Mar" in out
    assert "hit right drawer first, then left" in out
    assert "rule Memory has a validity date. The corpus does not." in out


def test_section_18_4_ast_chunking():
    page = (ROOT / "docs" / "mechanisms" / "ast_chunking.md").read_text(encoding="utf-8")
    assert "Not the Monday loop" in page
    assert "A function is the unit" in page
    assert "split through its return invents the type" in page
    assert "keeps the whole function in one chunk" in page
    assert "cAST" in page
    assert "tree-sitter" in page
    assert "Course identity stays enterprise documents" in page
    src = (
        ROOT / "notebooks/section_18_optional_2026_frontier_cards/classify_invoice.py"
    ).read_text(encoding="utf-8")
    assert "def classify_invoice" in src
    assert "-> LedgerReject" in src
    out = subprocess.run(
        [sys.executable, str(NB4)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    ).stdout
    assert "=== not a filing window ===" in out
    assert "file docs/mechanisms/ast_chunking.md" in out
    assert "split through the return" in out
    assert "left def classify_invoice(invoice_id: str) ->" in out
    assert "right LedgerReject:" in out
    assert "invented the model fills the type" in out
    assert "ast keeps the whole function" in out
    assert "name classify_invoice" in out
    assert "return LedgerReject" in out
    assert "rule A function is the unit." in out


def test_section_18_5_hot_ram():
    page = (ROOT / "docs" / "mechanisms" / "hot_ram_versus_object_store.md").read_text(encoding="utf-8")
    assert "Not the Monday loop" in page
    assert "Where the vectors live is a cost lever" in page
    assert "Hot HNSW RAM versus object-store cold" in page
    assert "Namespace equals tenant" in page
    assert "Hash before you re-embed" in page
    assert "No turbopuffer account" in page
    out = subprocess.run(
        [sys.executable, str(NB5)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    ).stdout
    assert "=== not generate tokens only ===" in out
    assert "file docs/mechanisms/hot_ram_versus_object_store.md" in out
    assert "hot RAM plus 3x SSD" in out
    assert "cold S3 plus SSD cache" in out
    assert "namespace helix-east ['faq']" in out
    assert "hash gate: embed" in out
    assert "hash gate: skip embed" in out
    assert "embed_calls 1" in out
    assert "rule Where the vectors live is a cost lever." in out
