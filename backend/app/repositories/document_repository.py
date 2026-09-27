from sqlalchemy.orm import Session

from app.db.models.document import Document


class DocumentRepository:

    def create(
        self,
        db: Session,
        document: Document
    ):
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    def get(
        self,
        db: Session,
        document_id: int
    ):
        return (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    def get_all(
        self,
        db: Session
    ):
        return (
            db.query(Document)
            .order_by(Document.uploaded_at.desc())
            .all()
        )
    def get_by_hash(
        self,
        db: Session,
        file_hash: str,
    ):

        return (
            db.query(Document)
            .filter(Document.file_hash == file_hash)
            .first()
        )

document_repository = DocumentRepository()