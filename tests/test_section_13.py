from rag.multimodal import caption_chunks, multimodal_chunks, parse_tables, smash_report
from rag.retrieve import bm25_search


def test_section_13_tables_and_captions():
    smash = smash_report()
    assert smash["has_12420"]
    parsed = parse_tables()
    assert parsed["parser"] in {"docling", "markdown-fallback"}
    assert any("12420" in r["text"] for r in parsed["rows"])
    assert "South 2000" in caption_chunks()[0].text
    hits = bm25_search("paid seats Q2", multimodal_chunks(), k=3)
    assert any("12420" in h.chunk.text for h in hits)
