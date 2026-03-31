from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    session_id: str | None = None


class Citation(BaseModel):
    id: str
    title: str
    snippet: str
    source: str
    page: int


class ChatResponse(BaseModel):
    answer: str
    mode: Literal["answer", "follow_up", "escalate"]
    risk_level: Literal["low", "medium", "high"]
    follow_up_question: str | None = None
    citations: list[Citation]
    disclaimer: str
    trace_id: str
