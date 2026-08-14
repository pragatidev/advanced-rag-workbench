from ragbench.index import build_index
from ragbench.settings import LAB_EMBEDDER
from ragbench.store import load_index, print_card


def test_build_index_writes_named_embedder_and_chunks(tmp_path):
    built = build_index("naive", root=tmp_path)
    assert (tmp_path / "naive" / "manifest.json").is_file()
    assert (tmp_path / "naive" / "chunks.jsonl").is_file()
    assert (tmp_path / "naive" / "vectors.npy").is_file()
    assert built.manifest["embedder"]["name"] == "ToyEmbedder"
    assert built.manifest["embedder"]["dim"] == LAB_EMBEDDER["dim"]
    assert built.manifest["chunker"] == "fixed"
    loaded = load_index("naive", root=tmp_path)
    assert loaded is not None
    assert len(loaded.chunks) == built.manifest["chunk_count"]
    card = print_card(loaded)
    assert "ToyEmbedder" in card
    assert "text-embedding-3-small" in card


def test_stored_dense_search_returns_hits(tmp_path):
    idx = build_index("naive", root=tmp_path)
    hits = idx.dense_search("What was ACME revenue growth in Q2 2023?", k=3)
    assert hits
    assert hits[0].chunk.text
