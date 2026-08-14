import json

from ragbench.cli import main


def test_ask_naive_json(capsys):
    code = main(["ask", "What does error code TS-999 mean?", "--pipeline", "naive"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["pipeline"] == "naive"
    assert "answer" in payload
    assert payload.get("generator", {}).get("generator") == "extractive"


def test_ask_refuses_chitchat(capsys):
    code = main(["ask", "Good morning, how are you?"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["answer"].startswith("REFUSE")
