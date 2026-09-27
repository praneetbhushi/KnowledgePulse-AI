from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    conversation_id: int | None = None
    top_k: int = 3
    max_distance: float | None = None
    document_id: int | None = None


class Source(BaseModel):
    document_id: int
    document_name: str
    chunk_index: int


class ChatResponse(BaseModel):
    question: str
    answer: str
    conversation_id: int
    sources: list[Source]