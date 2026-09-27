from app.services.document_processor import (
    document_processor
)

from app.services.text_processor import (
    text_processor
)


# Extract text from PDF
text = document_processor.extract_text(
    file_path="uploads/test.pdf",
    file_type="pdf"
)


print("=" * 50)
print("ORIGINAL TEXT")
print("=" * 50)

print(
    f"Original characters: {len(text)}"
)


# Clean text
cleaned_text = (
    text_processor.clean_text(
        text
    )
)


print("=" * 50)
print("CLEANED TEXT")
print("=" * 50)

print(
    f"Cleaned characters: {len(cleaned_text)}"
)


# Create chunks
chunks = (
    text_processor.chunk_text(
        cleaned_text,
        chunk_size=1000,
        chunk_overlap=200
    )
)


print("=" * 50)
print("CHUNKING RESULTS")
print("=" * 50)

print(
    f"Total chunks: {len(chunks)}"
)


for index, chunk in enumerate(
    chunks,
    start=1
):

    print(
        f"\n--- CHUNK {index} ---"
    )

    print(
        f"Characters: {len(chunk)}"
    )

    print(
        chunk[:200]
    )