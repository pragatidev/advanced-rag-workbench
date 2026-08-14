import json

from ragbench.ask import run_ask
from ragbench.cli import main


def test_ask_naive_json(capsys):
    code = main(["ask", "What does error code TS-999 mean?", "--pipeline", "naive"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["pipeline"] == "naive"
    assert "answer" in payload
    assert payload.get("generator", {}).get("generator") == "extractive"


def test_run_ask_is_the_product_function():
    payload = run_ask("What does error code TS-999 mean?", pipeline="hybrid", generate="extractive")
    blob = " ".join(h["text"] for h in payload["hits"]).lower()
    assert "ts-999" in blob


def test_ask_refuses_chitchat(capsys):
    code = main(["ask", "Good morning, how are you?"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["answer"].startswith("REFUSE")
