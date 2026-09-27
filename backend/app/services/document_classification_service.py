from typing import Dict

from app.services.embedding_service import (
    embedding_service
)


class DocumentClassificationService:

    def __init__(self):

        self.categories = {

            "Resume / CV":
            "Resumes, curriculum vitae, professional profiles, "
            "candidate information, skills, education, experience "
            "and career-related documents.",

            "HR Policy":
                "Human resources policies including employee "
                "leave, attendance, benefits, workplace rules, "
                "hiring and employee policies.",

            "Technical Documentation":
                "Technical documentation including software, "
                "hardware, system requirements, installation, "
                "configuration, APIs and engineering guides.",

            "SOP":
                "Standard operating procedures containing "
                "step-by-step operational instructions, "
                "processes and organizational procedures.",

            "Training Material":
                "Training, educational and learning material "
                "used to teach employees or students.",

            "Meeting Notes":
                "Meeting minutes, discussions, decisions, "
                "action items and meeting summaries.",

            "Finance":
                "Financial information including budgets, "
                "expenses, invoices, revenue, accounting "
                "and financial reports.",

            "Legal":
                "Legal documents including contracts, "
                "agreements, compliance policies, regulations "
                "and legal requirements.",

            "General":
                "General organizational information that does "
                "not clearly belong to another category."
        }

        self.category_names = list(
            self.categories.keys()
        )

        self.category_descriptions = list(
            self.categories.values()
        )

        # Generate category embeddings once
        self.category_embeddings = (
            embedding_service.generate_embeddings(
                self.category_descriptions
            )
        )


    def classify(
        self,
        text: str
    ) -> Dict:

        if not text or not text.strip():

            return {
                "category": "General",
                "confidence": 0.0
            }

        # Limit amount of text used for classification
        classification_text = text[:5000]

        document_embedding = (
            embedding_service.generate_embedding(
                classification_text
            )
        )

        # Calculate similarity with every category
        similarities = {}

        for category, category_embedding in zip(
            self.category_names,
            self.category_embeddings
        ):

            similarity = self._cosine_similarity(
                document_embedding,
                category_embedding
            )

            similarities[category] = similarity

        # Find category with highest similarity
        best_category = max(
            similarities,
            key=similarities.get
        )

        best_score = similarities[best_category]

        # Convert similarities into relative confidence
        # using softmax
        import math

        scores = list(similarities.values())

        max_score = max(scores)

        exp_scores = [
            math.exp(score - max_score)
            for score in scores
        ]

        total = sum(exp_scores)

        probabilities = [
            score / total
            for score in exp_scores
        ]

        best_index = scores.index(best_score)

        confidence = probabilities[best_index]

        return {
            "category": best_category,
            "confidence": round(
                float(confidence),
                4
            )
        }


    def _cosine_similarity(
        self,
        vector_a,
        vector_b
    ) -> float:

        dot_product = sum(
            a * b
            for a, b in zip(
                vector_a,
                vector_b
            )
        )

        magnitude_a = sum(
            a * a
            for a in vector_a
        ) ** 0.5

        magnitude_b = sum(
            b * b
            for b in vector_b
        ) ** 0.5

        if (
            magnitude_a == 0
            or magnitude_b == 0
        ):
            return 0.0

        return (
            dot_product
            / (
                magnitude_a
                * magnitude_b
            )
        )


document_classification_service = (
    DocumentClassificationService()
)