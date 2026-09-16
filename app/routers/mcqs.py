import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import MCQRequest, MCQResponse
from app.services import history_service, llm_service
from app.services.history_service import HistoryServiceError

router = APIRouter(prefix="/api/v1", tags=["mcqs"])


@router.post("/mcqs", response_model=MCQResponse)
def mcqs(payload: MCQRequest, db: Session = Depends(get_db)) -> MCQResponse:
    try:
        items, tokens_used = llm_service.generate_mcqs(payload.text, payload.num_questions)
        response = MCQResponse(id=0, mcqs=items, tokens_used=tokens_used)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=502, detail=f"Malformed LLM response: {exc}") from exc

    try:
        record = history_service.save(
            db,
            request_type="mcqs",
            input_text=payload.text,
            output_text=json.dumps(items),
            tokens_used=tokens_used,
        )
    except HistoryServiceError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    response.id = record.id
    return response
