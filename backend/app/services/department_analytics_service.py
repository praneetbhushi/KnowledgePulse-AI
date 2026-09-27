from collections import Counter

from sqlalchemy.orm import Session

from app.db.models.department import Department
from app.db.models.user import User
from app.db.models.document import Document


class DepartmentAnalyticsService:

    def get_department_analytics(
        self,
        db: Session,
        department_id: int
    ):

        # ---------------------------------
        # STEP 1: Find department
        # ---------------------------------

        department = (
            db.query(Department)
            .filter(
                Department.id == department_id
            )
            .first()
        )

        # ---------------------------------
        # STEP 2: Department does not exist
        # ---------------------------------

        if department is None:
            return None

        # ---------------------------------
        # STEP 3: Get department documents
        # ---------------------------------

        documents = (
            db.query(Document)
            .join(
                User,
                Document.uploaded_by == User.id
            )
            .filter(
                User.department_id == department_id
            )
            .all()
        )

        # ---------------------------------
        # STEP 4: Total documents
        # ---------------------------------

        total_documents = len(documents)

        # ---------------------------------
        # STEP 5: Get valid quality scores
        # ---------------------------------

        quality_scores = [
            float(document.quality_score)
            for document in documents
            if document.quality_score is not None
        ]

        # ---------------------------------
        # STEP 6: Average quality score
        # ---------------------------------

        if quality_scores:

            average_quality_score = (
                sum(quality_scores)
                / len(quality_scores)
            )

            average_quality_score = round(
                average_quality_score,
                2
            )

        else:

            average_quality_score = None

        # ---------------------------------
        # STEP 7: Category distribution
        # ---------------------------------

        categories = [
            document.category
            for document in documents
            if document.category is not None
        ]

        category_counter = Counter(
            categories
        )

        category_distribution = dict(
            category_counter
        )

        # ---------------------------------
        # STEP 8: Count duplicate documents
        # ---------------------------------

        duplicate_documents = sum(
            1
            for document in documents
            if document.is_duplicate is True
        )

        # ---------------------------------
        # STEP 9: Calculate duplicate rate
        # ---------------------------------

        if total_documents > 0:

            duplicate_rate = (
                duplicate_documents
                / total_documents
            ) * 100

            duplicate_rate = round(
                duplicate_rate,
                2
            )

        else:

            duplicate_rate = 0.0

        # ---------------------------------
        # STEP 10: Calculate uniqueness score
        # ---------------------------------

        uniqueness_score = (
            100 - duplicate_rate
        )

        # ---------------------------------
        # STEP 11: Knowledge Health Score
        # ---------------------------------

        if average_quality_score is not None:

            knowledge_health_score = (
                average_quality_score * 0.70
                +
                uniqueness_score * 0.30
            )

            knowledge_health_score = round(
                knowledge_health_score,
                2
            )

        else:

            knowledge_health_score = None

        # ---------------------------------
        # STEP 12: Knowledge Health Level
        # ---------------------------------

        if knowledge_health_score is None:

            knowledge_health_level = (
                "Not Available"
            )

        elif knowledge_health_score >= 80:

            knowledge_health_level = (
                "Excellent"
            )

        elif knowledge_health_score >= 60:

            knowledge_health_level = (
                "Good"
            )

        elif knowledge_health_score >= 40:

            knowledge_health_level = (
                "Fair"
            )

        else:

            knowledge_health_level = (
                "Poor"
            )

        # ---------------------------------
        # STEP 13: Return analytics
        # ---------------------------------

        return {
            "department_id":
                department.id,

            "department_name":
                department.name,

            "total_documents":
                total_documents,

            "documents_with_quality_score":
                len(quality_scores),

            "average_quality_score":
                average_quality_score,

            "category_distribution":
                category_distribution,

            "duplicate_documents":
                duplicate_documents,

            "duplicate_rate":
                duplicate_rate,

            "knowledge_health_score":
                knowledge_health_score,

            "knowledge_health_level":
                knowledge_health_level
        }


department_analytics_service = (
    DepartmentAnalyticsService()
)