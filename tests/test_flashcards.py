from unittest.mock import patch


def test_flashcards_success(client):
    mock_items = [{"front": "What is X?", "back": "X is Y"}]
    with patch(
        "app.routers.flashcards.llm_service.generate_flashcards",
        return_value=(mock_items, 15),
    ):
        r = client.post("/api/v1/flashcards", json={"text": "content", "num_cards": 1})

    assert r.status_code == 200
    assert r.json()["flashcards"] == mock_items
    assert r.json()["tokens_used"] == 15


def test_flashcards_malformed_llm_response_returns_502(client):
    with patch(
        "app.routers.flashcards.llm_service.generate_flashcards",
        return_value=([{"front": "Q1?"}], 5),  # missing 'back'
    ):
        r = client.post("/api/v1/flashcards", json={"text": "content"})
    assert r.status_code == 502


def test_flashcards_num_cards_out_of_range_rejected(client):
    r = client.post("/api/v1/flashcards", json={"text": "content", "num_cards": 0})
    assert r.status_code == 422
