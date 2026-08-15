import runpy
from pathlib import Path

from rag.pipelines.naive import NaivePipeline

ROOT = Path(__file__).resolve().parents[1]


def test_section_03_load_and_chunk(capsys):
    runpy.run_path(str(ROOT / "labs" / "lab_s3_naive" / "part_1" / "load_and_chunk.py"), run_name="__main__")
    out = capsys.readouterr().out.lower()
    assert "revenue grew by 3%" in out


def test_section_03_naive_pipeline():
    result = NaivePipeline()("What was ACME revenue growth in Q2 2023?")
    assert result["answer_source"] == "retrieved_text"
    assert result["hits"]
