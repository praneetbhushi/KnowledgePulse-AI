from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class SearchQuery(Base):
    __tablename__ = "search_queries"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    query: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    result_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    best_distance: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    search_time: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    llm_time: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    total_rag_time: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    was_answered: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    answer: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    searched_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    user = relationship(
        "User",
        back_populates="search_queries",
    )