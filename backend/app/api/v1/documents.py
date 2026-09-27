from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
)

from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.dependencies import (
    get_current_user
)

from app.schemas.document import (
    DocumentResponse
)

from app.services.document_service import (
    document_service
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post(
    "/upload",
    response_model=DocumentResponse
)
def upload_document(

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )

):

    return document_service.upload_document(

        db=db,

        file=file,

        user_id=current_user.id
    )