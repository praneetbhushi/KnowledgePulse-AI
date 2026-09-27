from sqlalchemy.orm import Session

from app.db.models.document import Document
from app.db.models.department import Department

from app.services.search_analytics_service import (
    search_analytics_service
)

from app.services.knowledge_gap_service import (
    knowledge_gap_service
)

from app.services.department_analytics_service import (
    department_analytics_service
)


class DashboardAnalyticsService:

    def get_dashboard_summary(
        self,
        db: Session
    ):

        # ---------------------------------
        # STEP 1
        # Get all documents
        # ---------------------------------

        documents = (
            db.query(Document)
            .all()
        )

        # ---------------------------------
        # STEP 2
        # Total documents
        # ---------------------------------

        total_documents = len(documents)

        # ---------------------------------
        # STEP 3
        # Processed documents
        # ---------------------------------

        processed_documents = sum(

            1

            for document in documents

            if document.status == "processed"

        )

        # ---------------------------------
        # STEP 4
        # Failed documents
        # ---------------------------------

        failed_documents = sum(

            1

            for document in documents

            if document.status == "failed"

        )

        # ---------------------------------
        # STEP 5
        # Processing documents
        # ---------------------------------

        processing_documents = sum(

            1

            for document in documents

            if document.status == "processing"

        )

        # ---------------------------------
        # STEP 6
        # Duplicate documents
        # ---------------------------------

        duplicate_documents = sum(

            1

            for document in documents

            if document.is_duplicate is True

        )

        # ---------------------------------
        # STEP 7
        # Quality scores
        # ---------------------------------

        quality_scores = [

            float(document.quality_score)

            for document in documents

            if document.quality_score is not None

        ]

        if quality_scores:

            average_quality_score = round(

                sum(quality_scores)
                /
                len(quality_scores),

                2

            )

        else:

            average_quality_score = None

        # ---------------------------------
        # STEP 8
        # Quality distribution
        # ---------------------------------

        excellent_documents = sum(

            1

            for document in documents

            if document.quality_level == "Excellent"

        )

        good_documents = sum(

            1

            for document in documents

            if document.quality_level == "Good"

        )

        fair_documents = sum(

            1

            for document in documents

            if document.quality_level == "Fair"

        )

        poor_documents = sum(

            1

            for document in documents

            if document.quality_level == "Poor"

        )

        documents_without_quality_score = sum(

            1

            for document in documents

            if document.quality_score is None

        )
                # ---------------------------------
        # STEP 9
        # Classified Documents
        # ---------------------------------

        classified_documents = [

            document

            for document in documents

            if document.category is not None

        ]

        total_classified_documents = len(
            classified_documents
        )

        # ---------------------------------
        # STEP 10
        # Classification Confidence
        # ---------------------------------

        confidence_scores = [

            float(document.classification_confidence)

            for document in classified_documents

            if document.classification_confidence
            is not None

        ]

        if confidence_scores:

            average_confidence = round(

                sum(confidence_scores)
                /
                len(confidence_scores),

                4

            )

        else:

            average_confidence = None

        # ---------------------------------
        # STEP 11
        # Category Distribution
        # ---------------------------------

        category_distribution = {}

        for document in classified_documents:

            category = document.category

            category_distribution[category] = (

                category_distribution.get(
                    category,
                    0
                )

                + 1

            )

        # ---------------------------------
        # STEP 12
        # Duplicate Rate
        # ---------------------------------

        if total_documents > 0:

            duplicate_rate = round(

                (
                    duplicate_documents
                    /
                    total_documents
                ) * 100,

                2

            )

        else:

            duplicate_rate = 0.0

        # ---------------------------------
        # STEP 13
        # Search Analytics
        # ---------------------------------

        search_analytics = (

            search_analytics_service.get_analytics(

                db=db

            )

        )

        # ---------------------------------
        # STEP 14
        # Knowledge Gap Analytics
        # ---------------------------------

        knowledge_gap_analytics = (

            knowledge_gap_service.get_gap_analytics(

                db=db

            )

        )
                # ---------------------------------
        # STEP 15
        # Department Health Analytics
        # ---------------------------------

        departments = (
            db.query(Department)
            .all()
        )

        department_health = []

        for department in departments:

            analytics = (
                department_analytics_service
                .get_department_analytics(
                    db=db,
                    department_id=department.id
                )
            )

            if analytics is not None:

                department_health.append(
                    analytics
                )

        # ---------------------------------
        # STEP 16
        # Department Health Summary
        # ---------------------------------

        total_departments = len(
            department_health
        )

        health_scores = [

            department[
                "knowledge_health_score"
            ]

            for department in department_health

            if department[
                "knowledge_health_score"
            ] is not None

        ]

        if health_scores:

            average_department_health = round(

                sum(
                    health_scores
                )
                /
                len(
                    health_scores
                ),

                2

            )

        else:

            average_department_health = None

        excellent_departments = sum(

            1

            for department in department_health

            if department[
                "knowledge_health_level"
            ] == "Excellent"

        )

        good_departments = sum(

            1

            for department in department_health

            if department[
                "knowledge_health_level"
            ] == "Good"

        )

        fair_departments = sum(

            1

            for department in department_health

            if department[
                "knowledge_health_level"
            ] == "Fair"

        )

        poor_departments = sum(

            1

            for department in department_health

            if department[
                "knowledge_health_level"
            ] == "Poor"

        )
                # ---------------------------------
        # STEP 17
        # Return Dashboard Summary
        # ---------------------------------

        return {

            "documents": {

                "total_documents":
                    total_documents,

                "processed_documents":
                    processed_documents,

                "failed_documents":
                    failed_documents,

                "processing_documents":
                    processing_documents,

                "duplicate_documents":
                    duplicate_documents

            },

            "quality": {

                "average_quality_score":
                    average_quality_score,

                "excellent_documents":
                    excellent_documents,

                "good_documents":
                    good_documents,

                "fair_documents":
                    fair_documents,

                "poor_documents":
                    poor_documents,

                "documents_without_quality_score":
                    documents_without_quality_score

            },

            "classification": {

                "total_classified_documents":
                    total_classified_documents,

                "average_classification_confidence":
                    average_confidence,

                "category_distribution":
                    category_distribution,

                "duplicate_rate":
                    duplicate_rate

            },

            "search_analytics": {

                "total_searches":
                    search_analytics["total_searches"],

                "unique_queries":
                    search_analytics["unique_queries"],

                "successful_searches":
                    search_analytics["successful_searches"],

                "weak_searches":
                    search_analytics["weak_searches"],

                "success_rate":
                    search_analytics["success_rate"],

                "average_best_distance":
                    search_analytics["average_best_distance"],

                "top_queries":
                    search_analytics["top_queries"]

            },

            "knowledge_gaps": {

                "total_gaps":
                    knowledge_gap_analytics["total_gaps"],

                "high_priority_gaps":
                    knowledge_gap_analytics["high_priority_gaps"],

                "medium_priority_gaps":
                    knowledge_gap_analytics["medium_priority_gaps"],

                "low_priority_gaps":
                    knowledge_gap_analytics["low_priority_gaps"],

                "average_gap_distance":
                    knowledge_gap_analytics["average_gap_distance"],

                "top_gaps":
                    knowledge_gap_analytics["top_gaps"]

            },

            "department_health": {

                "total_departments":
                    total_departments,

                "average_department_health":
                    average_department_health,

                "excellent_departments":
                    excellent_departments,

                "good_departments":
                    good_departments,

                "fair_departments":
                    fair_departments,

                "poor_departments":
                    poor_departments,

                "departments":
                    department_health

            }

        }
    
dashboard_analytics_service = DashboardAnalyticsService()