from app.services.document_processor import (
    document_processor
)

from app.services.text_processor import (
    text_processor
)

from app.services.embedding_service import (
    embedding_service
)
from sentence_transformers.util import cos_sim

# Step 1: Extract text
text = document_processor.extract_text(
    file_path="uploads/test.pdf",
    file_type="pdf"
)


# Step 2: Clean text
cleaned_text = text_processor.clean_text(
    text
)


# Step 3: Create chunks
chunks = text_processor.chunk_text(
    cleaned_text,
    chunk_size=1000,
    chunk_overlap=200
)


print("=" * 50)
print("CHUNKS")
print("=" * 50)

print(
    f"Total chunks: {len(chunks)}"
)


# Step 4: Generate embeddings
embeddings = (
    embedding_service.generate_embeddings(
        chunks
    )
)


print("=" * 50)
print("EMBEDDING RESULTS")
print("=" * 50)

print(
    f"Total embeddings: {len(embeddings)}"
)


if embeddings:

    print(
        f"Embedding dimensions: "
        f"{len(embeddings[0])}"
    )

    print(
        "First 10 values of first embedding:"
    )

    print(
        embeddings[0][:10]
    )
    query = (
    "What internet speed is required?"
)


query_embedding = (
    embedding_service.generate_embedding(
        query
    )
)


print("=" * 50)
print("SEMANTIC SIMILARITY")
print("=" * 50)


for index, embedding in enumerate(
    embeddings,
    start=1
):

    score = cos_sim(
        query_embedding,
        embedding
    )

    print(
        f"Chunk {index}: "
        f"{score.item():.4f}"
    )