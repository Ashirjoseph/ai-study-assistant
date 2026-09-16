from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class AskResponse(BaseModel):
    id: int
    question: str
    answer: str
    tokens_used: int | None = None


class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=8000)


class SummaryResponse(BaseModel):
    id: int
    summary: str
    tokens_used: int | None = None


class MCQItem(BaseModel):
    question: str
    options: list[str]
    answer_index: int


class MCQRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=8000)
    num_questions: int = Field(5, ge=1, le=10)


class MCQResponse(BaseModel):
    id: int
    mcqs: list[MCQItem]
    tokens_used: int | None = None


class FlashcardItem(BaseModel):
    front: str
    back: str


class FlashcardRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=8000)
    num_cards: int = Field(5, ge=1, le=10)


class FlashcardResponse(BaseModel):
    id: int
    flashcards: list[FlashcardItem]
    tokens_used: int | None = None


class HistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    request_type: str
    input_text: str
    output_text: str
    tokens_used: int | None = None
    created_at: datetime


class HistoryDeleteResponse(BaseModel):
    id: int
    deleted: bool
