from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import SummaryRequest, SummaryResponse
from app.services import history_service, llm_service
from app.services.history_service import HistoryServiceError

router = APIRouter(prefix="/api/v1", tags=["summary"])


@router.post("/summary", response_model=SummaryResponse)
def summary(payload: SummaryRequest, db: Session = Depends(get_db)) -> SummaryResponse:
    try:
        result = llm_service.generate_summary(payload.text)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    try:
        record = history_service.save(
            db,
            request_type="summary",
            input_text=payload.text,
            output_text=result.text,
            tokens_used=result.tokens_used,
        )
    except HistoryServiceError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return SummaryResponse(id=record.id, summary=result.text, tokens_used=result.tokens_used)
