from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.document import Document


router = APIRouter()


@router.get("/{document_id}")
def get_document_quality(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return {
        "document_id": document.id,
        "filename": document.original_filename,
        "quality_score": document.quality_score,
        "quality_level": document.quality_level,
        "is_duplicate": document.is_duplicate,
        "duplicate_similarity": document.duplicate_similarity,
        "category": document.category,
        "classification_confidence": (
            document.classification_confidence
        ),
    }