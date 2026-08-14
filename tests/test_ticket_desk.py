from examples.ticket_desk import handle_ticket


def test_ticket_handler_calls_run_ask():
    out = handle_ticket("T-1042", "What does error code TS-999 mean?")
    assert out["ticket_id"] == "T-1042"
    assert out["pipeline"] == "hybrid"
    assert out["sources"]
    assert "ts-999" in out["reply"].lower()
    assert not out["reply"].startswith("REFUSE")
