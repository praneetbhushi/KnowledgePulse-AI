from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    status: str
    category: str | None = None
    classification_confidence: float | None = None


class DocumentCreate(DocumentBase):
    file_path: str
    uploaded_by: int


class DocumentResponse(DocumentBase):
    id: int
    file_path: str
    uploaded_at: datetime
    uploaded_by: int

    model_config = ConfigDict(
        from_attributes=True
    )


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int


class DocumentUploadResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    status: str
    uploaded_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )