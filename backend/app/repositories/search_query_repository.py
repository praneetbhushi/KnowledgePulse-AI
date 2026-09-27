from sqlalchemy.orm import Session

from app.db.models.search_query import SearchQuery


class SearchQueryRepository:

    def create(
        self,
        db: Session,
        query: str,
        user_id: int,
        result_count: int,
        best_distance: float | None = None
    ) -> SearchQuery:

        search_query = SearchQuery(
            query=query,
            user_id=user_id,
            result_count=result_count,
            best_distance=best_distance
        )

        db.add(
            search_query
        )

        db.commit()

        db.refresh(
            search_query
        )

        return search_query


search_query_repository = (
    SearchQueryRepository()
)