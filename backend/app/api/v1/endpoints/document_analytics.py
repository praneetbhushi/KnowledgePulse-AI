from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.db.models.document import Document


router = APIRouter()


@router.get("/overview")
def get_document_overview(
    db: Session = Depends(get_db),
):
    total_documents = (
        db.query(func.count(Document.id))
        .scalar()
        or 0
    )

    processed_documents = (
        db.query(func.count(Document.id))
        .filter(Document.status == "processed")
        .scalar()
        or 0
    )

    duplicate_documents = (
        db.query(func.count(Document.id))
        .filter(Document.is_duplicate.is_(True))
        .scalar()
        or 0
    )

    average_quality = (
        db.query(func.avg(Document.quality_score))
        .filter(Document.quality_score.isnot(None))
        .scalar()
        or 0
    )

    return {
        "total_documents": total_documents,
        "processed_documents": processed_documents,
        "duplicate_documents": duplicate_documents,
        "average_quality": round(float(average_quality), 2),
    }
@router.get("/quality-distribution")
def get_quality_distribution(
    db: Session = Depends(get_db),
):
    results = (
        db.query(
            Document.quality_level,
            func.count(Document.id),
        )
        .filter(Document.quality_level.isnot(None))
        .group_by(Document.quality_level)
        .all()
    )

    return [
        {
            "quality_level": level,
            "count": count,
        }
        for level, count in results
    ]
@router.get("/recent")
def get_recent_documents(
    db: Session = Depends(get_db),
):
    documents = (
        db.query(Document)
        .order_by(Document.uploaded_at.desc())
        .limit(10)
        .all()
    )

    return [
        {
            "id": document.id,
            "filename": document.original_filename,
            "file_type": document.file_type,
            "status": document.status,
            "category": document.category,
            "quality_score": document.quality_score,
            "quality_level": document.quality_level,
            "is_duplicate": document.is_duplicate,
            "uploaded_at": document.uploaded_at,
        }
        for document in documents
    ]