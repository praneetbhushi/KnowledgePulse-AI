from collections import Counter

from sqlalchemy.orm import Session

from app.db.models.search_query import (
    SearchQuery
)

from datetime import datetime

class SearchAnalyticsService:

    # Same initial threshold used by
    # KnowledgeGapService.
    POOR_MATCH_DISTANCE = 0.8


    def get_analytics(
    self,
    db: Session,
    start_date: datetime | None = None,
    end_date: datetime | None = None
    ):

        # STEP 1: Build database query
        # ---------------------------------

        query = db.query(
            SearchQuery
        )


        # ---------------------------------
        # STEP 2: Apply start date filter
        # ---------------------------------

        if start_date is not None:

            query = query.filter(
                SearchQuery.searched_at
                >= start_date
            )


        # ---------------------------------
        # STEP 3: Apply end date filter
        # ---------------------------------

        if end_date is not None:

            query = query.filter(
                SearchQuery.searched_at
                <= end_date
            )


        # ---------------------------------
        # STEP 4: Execute query
        # ---------------------------------

        searches = query.all()


        # ---------------------------------
        # STEP 2: Handle empty database
        # ---------------------------------

        if not searches:

            return {
                "total_searches": 0,
                "unique_queries": 0,
                "successful_searches": 0,
                "weak_searches": 0,
                "success_rate": 0.0,
                "average_best_distance": None,
                "top_queries": []
            }


        # ---------------------------------
        # STEP 3: Total searches
        # ---------------------------------

        total_searches = len(
            searches
        )


        # ---------------------------------
        # STEP 4: Normalize queries
        # ---------------------------------

        normalized_queries = [

            search.query
            .strip()
            .lower()

            for search in searches
        ]


        # ---------------------------------
        # STEP 5: Unique query count
        # ---------------------------------

        unique_queries = len(
            set(
                normalized_queries
            )
        )


        # ---------------------------------
        # STEP 6:
        # Successful vs weak searches
        # ---------------------------------

        successful_searches = 0
        weak_searches = 0


        for search in searches:

            # No results means weak search
            if search.result_count == 0:

                weak_searches += 1

                continue


            # Missing distance means we
            # cannot confirm a good match
            if search.best_distance is None:

                weak_searches += 1

                continue


            # Large distance means
            # weak semantic match
            if (
                search.best_distance
                > self.POOR_MATCH_DISTANCE
            ):

                weak_searches += 1

            else:

                successful_searches += 1


        # ---------------------------------
        # STEP 7: Calculate success rate
        # ---------------------------------

        success_rate = (

            successful_searches
            / total_searches

        ) * 100


        success_rate = round(
            success_rate,
            2
        )


        # ---------------------------------
        # STEP 8:
        # Calculate average best distance
        # ---------------------------------

        valid_distances = [

            float(
                search.best_distance
            )

            for search in searches

            if search.best_distance
            is not None
        ]


        if valid_distances:

            average_best_distance = (
                sum(
                    valid_distances
                )
                /
                len(
                    valid_distances
                )
            )

            average_best_distance = round(
                average_best_distance,
                4
            )

        else:

            average_best_distance = None


        # ---------------------------------
        # STEP 9:
        # Find most frequently searched
        # queries
        # ---------------------------------

        query_counter = Counter(
            normalized_queries
        )


        most_common_queries = (
            query_counter
            .most_common(5)
        )


        top_queries = [

            {
                "query":
                    query,

                "search_count":
                    count
            }

            for query, count
            in most_common_queries
        ]


        # ---------------------------------
        # STEP 10:
        # Return analytics
        # ---------------------------------

        return {

            "total_searches":
                total_searches,

            "unique_queries":
                unique_queries,

            "successful_searches":
                successful_searches,

            "weak_searches":
                weak_searches,

            "success_rate":
                success_rate,

            "average_best_distance":
                average_best_distance,

            "top_queries":
                top_queries
        }


search_analytics_service = (
    SearchAnalyticsService()
)