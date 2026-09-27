class KnowledgeQualityService:
    
    def calculate_quality_score(
        self,
        text: str,
        classification_confidence: float | None,
        is_duplicate: bool
    ):

        # ---------------------------------
        # 1. Content Length Score
        # Maximum: 40 points
        # ---------------------------------

        text_length = len(
            text.strip()
        ) if text else 0

        if text_length >= 5000:
            length_score = 40

        elif text_length >= 2000:
            length_score = 35

        elif text_length >= 1000:
            length_score = 30

        elif text_length >= 500:
            length_score = 20

        elif text_length >= 100:
            length_score = 10

        else:
            length_score = 5


        # ---------------------------------
        # 2. Classification Confidence
        # Maximum: 30 points
        #
        # confidence is expected to be
        # between 0 and 1
        # ---------------------------------

        if classification_confidence is None:
            confidence_score = 0

        else:

            confidence = max(
                0.0,
                min(
                    float(
                        classification_confidence
                    ),
                    1.0
                )
            )

            confidence_score = (
                confidence * 30
            )


        # ---------------------------------
        # 3. Uniqueness Score
        # Maximum: 30 points
        # ---------------------------------

        if is_duplicate:
            uniqueness_score = 0

        else:
            uniqueness_score = 30


        # ---------------------------------
        # 4. Calculate Final Score
        # ---------------------------------

        quality_score = (
            length_score
            + confidence_score
            + uniqueness_score
        )

        quality_score = round(
            quality_score,
            2
        )


        # ---------------------------------
        # 5. Determine Quality Level
        # ---------------------------------

        if quality_score >= 80:
            quality_level = "Excellent"

        elif quality_score >= 60:
            quality_level = "Good"

        elif quality_score >= 40:
            quality_level = "Fair"

        else:
            quality_level = "Poor"


        # ---------------------------------
        # 6. Return Result
        # ---------------------------------

        return {
            "quality_score":
                quality_score,

            "quality_level":
                quality_level,

            "breakdown": {

                "length_score":
                    round(
                        length_score,
                        2
                    ),

                "classification_score":
                    round(
                        confidence_score,
                        2
                    ),

                "uniqueness_score":
                    round(
                        uniqueness_score,
                        2
                    )
            }
        }


knowledge_quality_service = (
    KnowledgeQualityService()
)