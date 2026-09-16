from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import HistoryDeleteResponse, HistoryItem
from app.services import history_service
from app.services.history_service import HistoryServiceError

router = APIRouter(prefix="/api/v1", tags=["history"])


@router.get("/history", response_model=list[HistoryItem])
def list_history(
    request_type: str | None = Query(None, description="Filter: ask|summary|mcqs|flashcards"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
) -> list[HistoryItem]:
    try:
        return history_service.list_items(db, request_type=request_type, limit=limit, offset=offset)
    except HistoryServiceError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/history/{item_id}", response_model=HistoryItem)
def get_history_item(item_id: int, db: Session = Depends(get_db)) -> HistoryItem:
    try:
        record = history_service.get_item(db, item_id)
    except HistoryServiceError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    if record is None:
        raise HTTPException(status_code=404, detail="History item not found")
    return record


@router.delete("/history/{item_id}", response_model=HistoryDeleteResponse)
def delete_history_item(item_id: int, db: Session = Depends(get_db)) -> HistoryDeleteResponse:
    try:
        deleted = history_service.delete_item(db, item_id)
    except HistoryServiceError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    if not deleted:
        raise HTTPException(status_code=404, detail="History item not found")
    return HistoryDeleteResponse(id=item_id, deleted=True)
