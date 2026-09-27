from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.document import Document


router = APIRouter()


@router.get("/{document_id}")
def get_document_intelligence(
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

        "file_type": document.file_type,

        "file_size": document.file_size,

        "status": document.status,

        "category": document.category,

        "classification_confidence": (
            document.classification_confidence
        ),

        "quality": {
            "score": document.quality_score,
            "level": document.quality_level,
        },

        "duplicate": {
            "is_duplicate": document.is_duplicate,
            "duplicate_of_document_id": (
                document.duplicate_of_document_id
            ),
            "similarity": (
                document.duplicate_similarity
            ),
        },

        "uploaded_at": document.uploaded_at,

        "uploaded_by": document.uploaded_by,
    }