from sqlalchemy.orm import Session

from app.repositories.analytics_repository import (
    analytics_repository
)


class AnalyticsService:

    def get_dashboard(
        self,
        db: Session,
    ):

        total_searches = (
            analytics_repository.get_total_searches(db)
        )

        answered_searches = (
            analytics_repository.get_answered_searches(db)
        )

        unanswered_searches = (
            analytics_repository.get_unanswered_searches(db)
        )

        answer_rate = 0.0

        if total_searches > 0:
            answer_rate = (
                answered_searches
                / total_searches
                * 100
            )

        return {
            "total_searches": total_searches,

            "answered_searches":
                answered_searches,

            "unanswered_searches":
                unanswered_searches,

            "answer_rate":
                round(answer_rate, 2),

            "average_search_time":
                round(
                    analytics_repository
                    .get_average_search_time(db),
                    2
                ),

            "average_llm_time":
                round(
                    analytics_repository
                    .get_average_llm_time(db),
                    2
                ),

            "average_rag_time":
                round(
                    analytics_repository
                    .get_average_rag_time(db),
                    2
                ),

            "average_distance":
                round(
                    analytics_repository
                    .get_average_distance(db),
                    3
                ),
        }


analytics_service = AnalyticsService()