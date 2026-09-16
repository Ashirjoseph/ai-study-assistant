from unittest.mock import patch

from app.services.llm_service import LLMResult


def test_ask_success(client):
    with patch(
        "app.routers.ask.llm_service.ask_question",
        return_value=LLMResult(text="42", tokens_used=10),
    ):
        r = client.post("/api/v1/ask", json={"question": "What is 6*7?"})

    assert r.status_code == 200
    body = r.json()
    assert body["answer"] == "42"
    assert body["tokens_used"] == 10
    assert isinstance(body["id"], int)


def test_ask_empty_question_rejected(client):
    r = client.post("/api/v1/ask", json={"question": ""})
    assert r.status_code == 422


def test_ask_llm_failure_returns_502(client):
    with patch(
        "app.routers.ask.llm_service.ask_question",
        side_effect=RuntimeError("LLM down"),
    ):
        r = client.post("/api/v1/ask", json={"question": "Q"})
    assert r.status_code == 502
