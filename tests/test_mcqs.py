from unittest.mock import patch


def test_mcqs_success(client):
    mock_items = [{"question": "Q1?", "options": ["A", "B", "C", "D"], "answer_index": 0}]
    with patch(
        "app.routers.mcqs.llm_service.generate_mcqs",
        return_value=(mock_items, 30),
    ):
        r = client.post("/api/v1/mcqs", json={"text": "content", "num_questions": 1})

    assert r.status_code == 200
    assert r.json()["mcqs"] == mock_items
    assert r.json()["tokens_used"] == 30


def test_mcqs_malformed_llm_response_returns_502(client):
    with patch(
        "app.routers.mcqs.llm_service.generate_mcqs",
        return_value=([{"question": "Q1?"}], 5),  # missing required fields
    ):
        r = client.post("/api/v1/mcqs", json={"text": "content"})
    assert r.status_code == 502


def test_mcqs_num_questions_out_of_range_rejected(client):
    r = client.post("/api/v1/mcqs", json={"text": "content", "num_questions": 50})
    assert r.status_code == 422
