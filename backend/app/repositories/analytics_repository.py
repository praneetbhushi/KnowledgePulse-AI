from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.models.search_query import SearchQuery


class AnalyticsRepository:

    def get_total_searches(
        self,
        db: Session,
    ) -> int:

        return (
            db.query(
                func.count(SearchQuery.id)
            )
            .scalar()
            or 0
        )

    def get_answered_searches(
        self,
        db: Session,
    ) -> int:

        return (
            db.query(
                func.count(SearchQuery.id)
            )
            .filter(
                SearchQuery.was_answered.is_(True)
            )
            .scalar()
            or 0
        )

    def get_unanswered_searches(
        self,
        db: Session,
    ) -> int:

        return (
            db.query(
                func.count(SearchQuery.id)
            )
            .filter(
                SearchQuery.was_answered.is_(False)
            )
            .scalar()
            or 0
        )

    def get_average_search_time(
        self,
        db: Session,
    ) -> float:

        return (
            db.query(
                func.avg(SearchQuery.search_time)
            )
            .filter(
                SearchQuery.search_time.isnot(None)
            )
            .scalar()
            or 0
        )

    def get_average_llm_time(
        self,
        db: Session,
    ) -> float:

        return (
            db.query(
                func.avg(SearchQuery.llm_time)
            )
            .filter(
                SearchQuery.llm_time.isnot(None)
            )
            .scalar()
            or 0
        )

    def get_average_rag_time(
        self,
        db: Session,
    ) -> float:

        return (
            db.query(
                func.avg(SearchQuery.total_rag_time)
            )
            .filter(
                SearchQuery.total_rag_time.isnot(None)
            )
            .scalar()
            or 0
        )

    def get_average_distance(
        self,
        db: Session,
    ) -> float:

        return (
            db.query(
                func.avg(SearchQuery.best_distance)
            )
            .filter(
                SearchQuery.best_distance.isnot(None)
            )
            .scalar()
            or 0
        )


analytics_repository = AnalyticsRepository()