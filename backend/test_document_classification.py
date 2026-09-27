from app.services.document_classification_service import (
    document_classification_service
)


test_text = """
Unstop SmartHire Installation and System Requirements Guide.

Students must install the SmartHire application before
the assessment.

The system requires a laptop or desktop with at least
8 GB RAM, a built-in webcam and microphone.

The recommended internet speed is 10 Mbps or higher.

Users must grant camera, microphone and screen recording
permissions before starting the assessment.
"""


result = (
    document_classification_service.classify(
        test_text
    )
)


print("=" * 50)
print("DOCUMENT CLASSIFICATION")
print("=" * 50)

print(
    f"Category: {result['category']}"
)

print(
    f"Confidence: {result['confidence']}"
)

print("=" * 50)