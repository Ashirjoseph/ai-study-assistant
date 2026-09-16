from unittest.mock import patch

from app.services.llm_service import LLMResult


def _create_ask(client, question="Q", answer="A", tokens=1):
    with patch(
        "app.routers.ask.llm_service.ask_question",
        return_value=LLMResult(text=answer, tokens_used=tokens),
    ):
        return client.post("/api/v1/ask", json={"question": question})


def test_history_list_and_get(client):
    r1 = _create_ask(client, question="Q1", answer="A1")
    r2 = _create_ask(client, question="Q2", answer="A2")
    assert r1.status_code == 200
    assert r2.status_code == 200

    r = client.get("/api/v1/history")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2

    item_id = items[0]["id"]
    r = client.get(f"/api/v1/history/{item_id}")
    assert r.status_code == 200
    assert r.json()["id"] == item_id


def test_history_get_missing_returns_404(client):
    r = client.get("/api/v1/history/9999")
    assert r.status_code == 404


def test_history_filter_by_request_type(client):
    _create_ask(client)
    r = client.get("/api/v1/history", params={"request_type": "ask"})
    assert r.status_code == 200
    assert all(item["request_type"] == "ask" for item in r.json())


def test_history_delete(client):
    r = _create_ask(client)
    item_id = r.json()["id"]

    r = client.delete(f"/api/v1/history/{item_id}")
    assert r.status_code == 200
    assert r.json() == {"id": item_id, "deleted": True}

    r = client.get(f"/api/v1/history/{item_id}")
    assert r.status_code == 404


def test_history_delete_missing_returns_404(client):
    r = client.delete("/api/v1/history/9999")
    assert r.status_code == 404
