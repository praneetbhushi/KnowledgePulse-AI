from app.services.document_processor import (
    document_processor
)

from app.services.text_processor import (
    text_processor
)

from app.services.embedding_service import (
    embedding_service
)

from app.services.vector_store_service import (
    vector_store_service
)


print("=" * 50)
print("STEP 1: EXTRACT TEXT")
print("=" * 50)

text = document_processor.extract_text(
    file_path="uploads/test.pdf",
    file_type="pdf"
)

print(
    f"Extracted characters: {len(text)}"
)


print("=" * 50)
print("STEP 2: CLEAN TEXT")
print("=" * 50)

cleaned_text = text_processor.clean_text(
    text
)

print(
    f"Cleaned characters: {len(cleaned_text)}"
)


print("=" * 50)
print("STEP 3: CREATE CHUNKS")
print("=" * 50)

chunks = text_processor.chunk_text(
    cleaned_text,
    chunk_size=1000,
    chunk_overlap=200
)

print(
    f"Total chunks: {len(chunks)}"
)


print("=" * 50)
print("STEP 4: GENERATE EMBEDDINGS")
print("=" * 50)

embeddings = (
    embedding_service.generate_embeddings(
        chunks
    )
)

print(
    f"Total embeddings: {len(embeddings)}"
)


print("=" * 50)
print("STEP 5: STORE IN CHROMADB")
print("=" * 50)

vector_store_service.add_document_chunks(
    document_id=1,
    chunks=chunks,
    embeddings=embeddings
)

print(
    "Chunks stored successfully."
)


print("=" * 50)
print("STEP 6: SEMANTIC SEARCH")
print("=" * 50)

query = (
    "What internet speed is required?"
)

print(
    f"Query: {query}"
)


query_embedding = (
    embedding_service.generate_embedding(
        query
    )
)


results = vector_store_service.search(
    query_embedding=query_embedding,
    n_results=3
)


print("=" * 50)
print("SEARCH RESULTS")
print("=" * 50)


documents = results.get(
    "documents",
    [[]]
)[0]

metadatas = results.get(
    "metadatas",
    [[]]
)[0]

distances = results.get(
    "distances",
    [[]]
)[0]


for index, document in enumerate(
    documents
):

    print(
        f"\n--- RESULT {index + 1} ---"
    )

    print(
        f"Metadata: {metadatas[index]}"
    )

    print(
        f"Distance: {distances[index]}"
    )

    print(
        "Content:"
    )

    print(
        document[:500]
    )