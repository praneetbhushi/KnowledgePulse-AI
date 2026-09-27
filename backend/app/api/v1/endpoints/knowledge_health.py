from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.db.models.document import Document


router = APIRouter()


@router.get("/summary")
def get_knowledge_health_summary(
    db: Session = Depends(get_db),
):
    # -----------------------------------------
    # Total documents
    # -----------------------------------------

    total_documents = (
        db.query(func.count(Document.id))
        .scalar()
        or 0
    )

    # -----------------------------------------
    # Successfully processed documents
    # -----------------------------------------

    processed_documents = (
        db.query(func.count(Document.id))
        .filter(Document.status == "processed")
        .scalar()
        or 0
    )

    # -----------------------------------------
    # Documents currently uploaded
    # -----------------------------------------

    uploaded_documents = (
        db.query(func.count(Document.id))
        .filter(Document.status == "uploaded")
        .scalar()
        or 0
    )

    # -----------------------------------------
    # Duplicate documents
    # -----------------------------------------

    duplicate_documents = (
        db.query(func.count(Document.id))
        .filter(Document.is_duplicate.is_(True))
        .scalar()
        or 0
    )

    # -----------------------------------------
    # Classified documents
    # -----------------------------------------

    classified_documents = (
        db.query(func.count(Document.id))
        .filter(Document.category.isnot(None))
        .filter(Document.category != "")
        .scalar()
        or 0
    )

    # -----------------------------------------
    # Documents without classification
    # -----------------------------------------

    unclassified_documents = (
        total_documents - classified_documents
    )

    # -----------------------------------------
    # Documents with quality score
    # -----------------------------------------

    scored_documents = (
        db.query(func.count(Document.id))
        .filter(Document.quality_score.isnot(None))
        .scalar()
        or 0
    )

    # -----------------------------------------
    # Average quality score
    # -----------------------------------------

    average_quality_score = (
        db.query(func.avg(Document.quality_score))
        .filter(Document.quality_score.isnot(None))
        .scalar()
        or 0
    )

    # -----------------------------------------
    # High quality documents
    # -----------------------------------------

    high_quality_documents = (
        db.query(func.count(Document.id))
        .filter(Document.quality_score >= 80)
        .scalar()
        or 0
    )

    # -----------------------------------------
    # Medium quality documents
    # -----------------------------------------

    medium_quality_documents = (
        db.query(func.count(Document.id))
        .filter(
            Document.quality_score >= 50,
            Document.quality_score < 80,
        )
        .scalar()
        or 0
    )

    # -----------------------------------------
    # Low quality documents
    # -----------------------------------------

    low_quality_documents = (
        db.query(func.count(Document.id))
        .filter(Document.quality_score < 50)
        .scalar()
        or 0
    )

    # -----------------------------------------
    # Category distribution
    # -----------------------------------------

    category_rows = (
        db.query(
            Document.category,
            func.count(Document.id),
        )
        .filter(Document.category.isnot(None))
        .group_by(Document.category)
        .order_by(func.count(Document.id).desc())
        .all()
    )

    categories = [
        {
            "category": category,
            "count": count,
        }
        for category, count in category_rows
    ]

    # -----------------------------------------
    # File type distribution
    # -----------------------------------------

    file_type_rows = (
        db.query(
            Document.file_type,
            func.count(Document.id),
        )
        .group_by(Document.file_type)
        .order_by(func.count(Document.id).desc())
        .all()
    )

    file_types = [
        {
            "file_type": file_type,
            "count": count,
        }
        for file_type, count in file_type_rows
    ]

    # -----------------------------------------
    # Overall health score
    #
    # Currently based on:
    # - quality score
    # - classification coverage
    # - duplicate rate
    #
    # This will be expanded later.
    # -----------------------------------------

    quality_component = (
        float(average_quality_score)
        if scored_documents > 0
        else 0
    )

    classification_component = (
        (classified_documents / total_documents) * 100
        if total_documents > 0
        else 0
    )

    duplicate_component = (
        100 - ((duplicate_documents / total_documents) * 100)
        if total_documents > 0
        else 100
    )

    overall_health_score = (
        quality_component * 0.50
        + classification_component * 0.30
        + duplicate_component * 0.20
    )

    # -----------------------------------------
    # Health level
    # -----------------------------------------

    if overall_health_score >= 80:
        health_level = "Excellent"
    elif overall_health_score >= 60:
        health_level = "Good"
    elif overall_health_score >= 40:
        health_level = "Needs Attention"
    else:
        health_level = "Critical"

    return {
        "total_documents": total_documents,
        "processed_documents": processed_documents,
        "uploaded_documents": uploaded_documents,
        "duplicate_documents": duplicate_documents,
        "classified_documents": classified_documents,
        "unclassified_documents": unclassified_documents,
        "scored_documents": scored_documents,
        "average_quality_score": round(
            float(average_quality_score),
            2,
        ),
        "high_quality_documents": high_quality_documents,
        "medium_quality_documents": medium_quality_documents,
        "low_quality_documents": low_quality_documents,
        "overall_health_score": round(
            overall_health_score,
            2,
        ),
        "health_level": health_level,
        "categories": categories,
        "file_types": file_types,
    }