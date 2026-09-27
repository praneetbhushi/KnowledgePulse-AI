from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Document(Base):

    __tablename__ = "documents"

    # --------------------------------------------------
    # Primary Key
    # --------------------------------------------------

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # --------------------------------------------------
    # File Information
    # --------------------------------------------------

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    # SHA-256 hash used for duplicate-file detection
    file_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
    )

    # --------------------------------------------------
    # Processing Status
    # --------------------------------------------------

    status: Mapped[str] = mapped_column(
        String(30),
        default="uploaded",
        nullable=False,
    )

    # --------------------------------------------------
    # Document Classification
    # --------------------------------------------------

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    classification_confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # --------------------------------------------------
    # Duplicate Detection
    # --------------------------------------------------

    is_duplicate: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    duplicate_of_document_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "documents.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    duplicate_similarity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # --------------------------------------------------
    # Document Quality
    # --------------------------------------------------

    quality_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    quality_level: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    # --------------------------------------------------
    # Upload Information
    # --------------------------------------------------

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )

    # --------------------------------------------------
    # Relationships
    # --------------------------------------------------

    uploader = relationship(
        "User",
        back_populates="documents",
    )