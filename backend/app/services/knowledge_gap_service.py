from collections import defaultdict

from sqlalchemy.orm import Session

from app.db.models.search_query import SearchQuery


class KnowledgeGapService:

    # ---------------------------------
    # Distance threshold
    #
    # Higher distance = weaker match
    # ---------------------------------

    POOR_MATCH_DISTANCE = 0.8


    # ---------------------------------
    # Check whether one search
    # represents a knowledge gap
    # ---------------------------------

    def is_knowledge_gap(
        self,
        result_count: int,
        best_distance: float | None
    ) -> bool:

        # Case 1:
        # No search results
        if result_count == 0:
            return True

        # Case 2:
        # No distance available
        if best_distance is None:
            return True

        # Case 3:
        # Weak semantic match
        if (
            best_distance
            > self.POOR_MATCH_DISTANCE
        ):
            return True

        return False


    # ---------------------------------
    # Detect + aggregate knowledge gaps
    # ---------------------------------

    def get_knowledge_gaps(
        self,
        db: Session,
        limit: int = 100
    ):

        # ---------------------------------
        # STEP 1:
        # Get recent search queries
        # ---------------------------------

        search_queries = (
            db.query(
                SearchQuery
            )
            .order_by(
                SearchQuery.searched_at.desc()
            )
            .limit(
                limit
            )
            .all()
        )


        # ---------------------------------
        # STEP 2:
        # Create grouping structure
        # ---------------------------------

        grouped_gaps = defaultdict(
            lambda: {
                "count": 0,
                "distances": [],
                "latest_search": None,
                "query": None
            }
        )


        # ---------------------------------
        # STEP 3:
        # Analyze every search
        # ---------------------------------

        for search_query in search_queries:

            gap_detected = (
                self.is_knowledge_gap(
                    result_count=(
                        search_query.result_count
                    ),
                    best_distance=(
                        search_query.best_distance
                    )
                )
            )


            # Ignore searches that have
            # good knowledge coverage
            if not gap_detected:
                continue


            # ---------------------------------
            # Normalize the query
            #
            # Example:
            #
            # "Company VPN Setup"
            # "company vpn setup"
            #
            # become the same group.
            # ---------------------------------

            normalized_query = (
                search_query.query
                .strip()
                .lower()
            )


            # Get this query's group
            gap = grouped_gaps[
                normalized_query
            ]


            # ---------------------------------
            # Increase occurrence count
            # ---------------------------------

            gap["count"] += 1


            # ---------------------------------
            # Store original query
            # ---------------------------------

            gap["query"] = (
                search_query.query
            )


            # ---------------------------------
            # Store valid semantic distance
            # ---------------------------------

            if (
                search_query.best_distance
                is not None
            ):

                gap["distances"].append(
                    float(
                        search_query.best_distance
                    )
                )


            # ---------------------------------
            # Store latest search timestamp
            # ---------------------------------

            if (
                gap["latest_search"]
                is None
                or
                search_query.searched_at
                > gap["latest_search"]
            ):

                gap["latest_search"] = (
                    search_query.searched_at
                )


        # ---------------------------------
        # STEP 4:
        # Build final knowledge gap list
        # ---------------------------------

        knowledge_gaps = []


        for gap in grouped_gaps.values():

            occurrence_count = (
                gap["count"]
            )


            # ---------------------------------
            # Calculate average distance
            # ---------------------------------

            if gap["distances"]:

                average_distance = (
                    sum(
                        gap["distances"]
                    )
                    /
                    len(
                        gap["distances"]
                    )
                )

                average_distance = round(
                    average_distance,
                    4
                )

            else:

                average_distance = None


            # ---------------------------------
            # STEP 5:
            # Assign priority
            #
            # 1-2 searches = Low
            # 3-4 searches = Medium
            # 5+ searches  = High
            # ---------------------------------

            if occurrence_count >= 5:

                priority = "High"

            elif occurrence_count >= 3:

                priority = "Medium"

            else:

                priority = "Low"


            # ---------------------------------
            # STEP 6:
            # Add aggregated knowledge gap
            # ---------------------------------

            knowledge_gaps.append(
                {
                    "query":
                        gap["query"],

                    "occurrence_count":
                        occurrence_count,

                    "average_distance":
                        average_distance,

                    "priority":
                        priority,

                    "latest_search":
                        gap["latest_search"]
                }
            )


        # ---------------------------------
        # STEP 7:
        # Sort by occurrence count
        #
        # Most frequently searched
        # knowledge gaps appear first
        # ---------------------------------

        knowledge_gaps.sort(
            key=lambda item:
                item[
                    "occurrence_count"
                ],
            reverse=True
        )


        # ---------------------------------
        # STEP 8:
        # Return aggregated gaps
        # ---------------------------------

        return knowledge_gaps

    def get_gap_analytics(
    self,
    db: Session
):

        knowledge_gaps = self.get_knowledge_gaps(db)

        total_gaps = len(knowledge_gaps)

        high_priority_gaps = sum(
            1
            for gap in knowledge_gaps
            if gap["priority"] == "High"
        )

        medium_priority_gaps = sum(
            1
            for gap in knowledge_gaps
            if gap["priority"] == "Medium"
        )

        low_priority_gaps = sum(
            1
            for gap in knowledge_gaps
            if gap["priority"] == "Low"
        )

        distances = [

            gap["average_distance"]

            for gap in knowledge_gaps

            if gap["average_distance"] is not None

        ]

        average_gap_distance = (

            round(
                sum(distances) / len(distances),
                4
            )

            if distances

            else None

        )

        return {

            "total_gaps": total_gaps,

            "high_priority_gaps": high_priority_gaps,

            "medium_priority_gaps": medium_priority_gaps,

            "low_priority_gaps": low_priority_gaps,

            "average_gap_distance": average_gap_distance,

            "top_gaps": knowledge_gaps[:5]

        }


# ---------------------------------
# Create service instance
# ---------------------------------
knowledge_gap_service = KnowledgeGapService()