from fastapi import APIRouter, UploadFile, File, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.core.dependencies import get_current_user

from app.schemas.document import (
    DocumentUploadResponse,
    DocumentResponse,
)

from app.services.document_service import document_service


router = APIRouter()


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return document_service.upload_document(
        db=db,
        file=file,
        user_id=current_user.id,
    )


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def get_documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return document_service.get_documents(db)