# AI Study Assistant — Backend

FastAPI backend that answers study questions, generates summaries/MCQs/flashcards
via an LLM, and stores/retrieves history in SQLite.

## Structure

```text
app/
  main.py            FastAPI app, router registration, global error handler
  config.py          Env-based settings (pydantic-settings)
  database.py        SQLAlchemy engine/session, init_db()
  models.py          History ORM model
  schemas.py         Pydantic request/response models
  routers/           One file per resource — HTTP layer only
    ask.py
    summary.py
    mcqs.py
    flashcards.py
    history.py
  services/
    llm_service.py       All LLM calls (isolated, mockable, one call per feature)
    history_service.py   All DB access for history (isolated from routers)
tests/               Pytest suite (LLM always mocked)
postman/             Postman collection + local environment
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt   # includes requirements.txt + pytest/httpx
cp .env.example .env
# edit .env and set LLM_API_KEY
```

## Run

```bash
uvicorn app.main:app --reload
```

Server: http://localhost:8000 — Swagger UI: http://localhost:8000/docs

## Run tests

```bash
pytest -v
```

Tests never call the real LLM — `llm_service` functions are mocked in every test,
and the DB is an isolated in-memory SQLite instance per test run.

## Configuration (`.env`)

| Variable | Default | Notes |
|---|---|---|
| `APP_ENV` | `development` | |
| `DATABASE_URL` | `sqlite:///./study_assistant.db` | |
| `LLM_API_KEY` | — | required for real LLM calls |
| `LLM_MODEL` | `gpt-4o-mini` | use a low-cost model in dev |
| `LLM_MAX_TOKENS` | `400` | hard cap per LLM call |
| `LLM_BASE_URL` | unset | optional, for OpenAI-compatible providers |

## API Reference

All endpoints are prefixed `/api/v1` except `/health`.

| Method | Path | Body | Notes |
|---|---|---|---|
| GET | `/health` | — | liveness check |
| POST | `/ask` | `{"question": str}` | AI explanation |
| POST | `/summary` | `{"text": str}` | 3–5 bullet summary |
| POST | `/mcqs` | `{"text": str, "num_questions": 1-10}` | structured JSON MCQs |
| POST | `/flashcards` | `{"text": str, "num_cards": 1-10}` | structured JSON flashcards |
| GET | `/history` | — | query: `request_type`, `limit` (≤100), `offset` |
| GET | `/history/{id}` | — | 404 if missing |
| DELETE | `/history/{id}` | — | 404 if missing |

**Example**

```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a binary search tree?"}'
```

```json
{
  "id": 1,
  "question": "What is a binary search tree?",
  "answer": "...",
  "tokens_used": 87
}
```

## Postman

Import `postman/AI_Study_Assistant.postman_collection.json` and
`postman/local.postman_environment.json`, select the **Local** environment,
and run requests against a running server.

## Design notes / LLM token optimization

- One LLM call per feature; no conversation history is sent (each request is stateless).
- Concise, single-purpose system prompts.
- `LLM_MAX_TOKENS` caps every call (configurable via `.env`).
- MCQs/flashcards use JSON response mode (`response_format={"type": "json_object"}`)
  instead of parsing free text, and are validated against a Pydantic schema; a malformed
  LLM response returns `502` instead of a raw crash.
- Token usage (`tokens_used`) is captured from the API response and stored with each
  history row when the provider reports it.
- Errors are mapped explicitly: `422` invalid input, `404` missing history item,
  `502` LLM failure/malformed output, `500` DB failure or unexpected error
  (generic message only — no internals leaked).
