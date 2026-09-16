from unittest.mock import patch

from app.services.llm_service import LLMResult


def test_summary_success(client):
    with patch(
        "app.routers.summary.llm_service.generate_summary",
        return_value=LLMResult(text="- point one\n- point two", tokens_used=25),
    ):
        r = client.post("/api/v1/summary", json={"text": "Some study material"})

    assert r.status_code == 200
    body = r.json()
    assert body["summary"] == "- point one\n- point two"
    assert body["tokens_used"] == 25


def test_summary_empty_text_rejected(client):
    r = client.post("/api/v1/summary", json={"text": ""})
    assert r.status_code == 422


def test_summary_llm_failure_returns_502(client):
    with patch(
        "app.routers.summary.llm_service.generate_summary",
        side_effect=RuntimeError("LLM down"),
    ):
        r = client.post("/api/v1/summary", json={"text": "content"})
    assert r.status_code == 502
