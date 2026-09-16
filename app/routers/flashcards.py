import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import FlashcardRequest, FlashcardResponse
from app.services import history_service, llm_service
from app.services.history_service import HistoryServiceError

router = APIRouter(prefix="/api/v1", tags=["flashcards"])


@router.post("/flashcards", response_model=FlashcardResponse)
def flashcards(payload: FlashcardRequest, db: Session = Depends(get_db)) -> FlashcardResponse:
    try:
        items, tokens_used = llm_service.generate_flashcards(payload.text, payload.num_cards)
        response = FlashcardResponse(id=0, flashcards=items, tokens_used=tokens_used)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=502, detail=f"Malformed LLM response: {exc}") from exc

    try:
        record = history_service.save(
            db,
            request_type="flashcards",
            input_text=payload.text,
            output_text=json.dumps(items),
            tokens_used=tokens_used,
        )
    except HistoryServiceError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    response.id = record.id
    return response
