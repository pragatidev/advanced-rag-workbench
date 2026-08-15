import runpy
from pathlib import Path

from rag.chunking.semantic import cosine_breakpoint_chunks
from rag.corpus import load_documents

ROOT = Path(__file__).resolve().parents[1]


def test_section_05_chunkers(capsys):
    runpy.run_path(str(ROOT / "labs" / "lab_s5_chunk" / "part_1" / "fixed_and_recursive.py"), run_name="__main__")
    out = capsys.readouterr().out
    assert "recursive" in out
    docs = {d.doc_id: d for d in load_documents()}
    sem = cosine_breakpoint_chunks(docs["filing_q2_2023"])
    assert sem
