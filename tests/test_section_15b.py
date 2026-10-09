from rag.cutover import DualColumnIndex, VersionedEmbedder
from rag.embed import ToyEmbedder, cosine
from rag.incremental import DerivedIndex, stable_chunk_key


def test_section_15b_upsert_tombstone_hides_stale():
    idx = DerivedIndex(ToyEmbedder(semantic_mode=False))
    for i in range(3):
        idx.upsert(f"doc_{i}", f"warehouse file {i} is unchanged padding about seats and revenue.")
    old_text = "Retention is thirty days. That line is the old policy."
    new_text = "Retention is seven days. That line is the live policy."
    old_id = idx.upsert("policy", old_text)
    assert old_id == stable_chunk_key("policy", old_text)
    before = idx.embed_calls
    new_id = idx.upsert("policy", new_text)
    idx.tombstone(old_id)
    assert idx.embed_calls - before == 1
    assert new_id != old_id
    hits = idx.retrieve("retention is thirty days", k=5)
    ids = [h[0] for h in hits]
    assert old_id not in ids
    assert new_id in ids
    assert hits[0][0] == new_id


def test_section_15b_mixed_space_returns_number_no_error():
    chunks = [
        ("policy", "Retention is seven days. That line is the live policy."),
        ("warehouse_00", "Warehouse throughput improved. Marketing spend was steady."),
        ("error_catalog", "TS-999 means the billing ledger rejected a duplicate invoice ID."),
        ("privacy", "Customer email, phone, and national id are PII. Redact national id."),
        ("access", "Least privilege. Support may read email. National id stays redacted."),
        ("faq", "Reset the token, then retry the invoice. Do not invent a new id."),
        ("kpis", "Q2 seats east 4100 west 3900 north 2420 south 2000."),
        ("warehouse_01", "Seats by region east west north south. Padding about capacity."),
    ]
    idx = DualColumnIndex()
    idx.fill_column("v1", chunks, VersionedEmbedder("v1"))
    idx.fill_column("v3", chunks, VersionedEmbedder("v3"))
    query = "retention is seven days"
    same_hits, same_meta = idx.retrieve(query, "v1", column="v1", k=3)
    mix_hits, mix_meta = idx.retrieve(query, "v3", column="v1", k=3)
    assert same_meta["error_raised"] is False
    assert mix_meta["error_raised"] is False
    assert mix_meta["mixed"] is True
    assert same_hits[0][0] == "policy"
    assert mix_hits[0][0] != same_hits[0][0]
    same_text = chunks[0][1]
    v1 = VersionedEmbedder("v1")
    v3 = VersionedEmbedder("v3")
    assert abs(float(cosine(v1.embed(same_text), v3.embed(same_text)))) < 0.3


def test_section_15b_dual_column_flip_serves_matching_space():
    chunks = [
        ("policy", "Retention is seven days. That line is the live policy."),
        ("warehouse_00", "Warehouse throughput improved. Marketing spend was steady."),
        ("error_catalog", "TS-999 means the billing ledger rejected a duplicate invoice ID."),
        ("privacy", "Customer email, phone, and national id are PII. Redact national id."),
        ("access", "Least privilege. Support may read email. National id stays redacted."),
        ("faq", "Reset the token, then retry the invoice. Do not invent a new id."),
        ("kpis", "Q2 seats east 4100 west 3900 north 2420 south 2000."),
        ("warehouse_01", "Seats by region east west north south. Padding about capacity."),
    ]
    idx = DualColumnIndex()
    idx.fill_column("v1", chunks, VersionedEmbedder("v1"))
    idx.fill_column("v3", chunks, VersionedEmbedder("v3"))
    assert idx.live == "v1"
    idx.flip("v3")
    assert idx.live == "v3"
    hits, meta = idx.retrieve("retention is seven days", "v3", k=1)
    assert meta["error_raised"] is False
    assert meta["mixed"] is False
    assert meta["column"] == "v3"
    assert hits[0][0] == "policy"
