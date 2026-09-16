from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AskRequest, AskResponse
from app.services import history_service, llm_service
from app.services.history_service import HistoryServiceError

router = APIRouter(prefix="/api/v1", tags=["ask"])


@router.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest, db: Session = Depends(get_db)) -> AskResponse:
    try:
        result = llm_service.ask_question(payload.question)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    try:
        record = history_service.save(
            db,
            request_type="ask",
            input_text=payload.question,
            output_text=result.text,
            tokens_used=result.tokens_used,
        )
    except HistoryServiceError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return AskResponse(
        id=record.id,
        question=payload.question,
        answer=result.text,
        tokens_used=result.tokens_used,
    )
