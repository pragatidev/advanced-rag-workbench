from rag.loops.retrieve_gate import needs_corpus, support_or_refuse
from rag.query.router import route


def test_section_10_gate_and_router():
    assert needs_corpus("Good morning, how are you?") is False
    assert needs_corpus("What does error code TS-999 mean?") is True
    ctx = ["TS-999 means the billing ledger rejected a duplicate invoice id."]
    assert not support_or_refuse("The CEO moved to Mars.", ctx).startswith("TS")
    assert route("Good morning, how are you?")["route"] == "none"
    assert route("What does error code TS-999 mean?")["route"] == "source"
    assert route("What are the main themes in this ACME corpus?")["route"] == "multi"
    assert route("What was ACME revenue growth in Q2 2023?")["route"] == "single"
