from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import History


class HistoryServiceError(Exception):
    """Raised when a database operation on history records fails."""


def save(
    db: Session,
    *,
    request_type: str,
    input_text: str,
    output_text: str,
    tokens_used: int | None,
) -> History:
    record = History(
        request_type=request_type,
        input_text=input_text,
        output_text=output_text,
        tokens_used=tokens_used,
    )
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HistoryServiceError("Failed to save history record") from exc
    return record


def list_items(db: Session, *, request_type: str | None, limit: int, offset: int) -> list[History]:
    stmt = select(History).order_by(History.created_at.desc()).offset(offset).limit(limit)
    if request_type:
        stmt = stmt.where(History.request_type == request_type)
    try:
        return list(db.execute(stmt).scalars().all())
    except SQLAlchemyError as exc:
        raise HistoryServiceError("Failed to fetch history") from exc


def get_item(db: Session, item_id: int) -> History | None:
    try:
        return db.get(History, item_id)
    except SQLAlchemyError as exc:
        raise HistoryServiceError("Failed to fetch history item") from exc


def delete_item(db: Session, item_id: int) -> bool:
    record = get_item(db, item_id)
    if record is None:
        return False
    try:
        db.delete(record)
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HistoryServiceError("Failed to delete history item") from exc
    return True
