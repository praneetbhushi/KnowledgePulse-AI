from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import rag_service

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    return rag_service.answer_question(
    db=db,
    question=request.question,
    top_k=request.top_k,
    max_distance=request.max_distance,
    document_id=request.document_id,
)