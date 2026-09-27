from app.services.vector_store_service import (
    vector_store_service
)


print("=" * 50)
print("CHROMADB VERIFICATION")
print("=" * 50)


# Total vectors in collection
count = (
    vector_store_service
    .get_collection_count()
)

print(
    "Total vectors stored:",
    count
)


# Get vectors/chunks belonging to document ID 1
results = (
    vector_store_service
    .collection
    .get(
        where={
            "document_id": 1
        }
    )
)


print("=" * 50)
print("DOCUMENT 1 RESULTS")
print("=" * 50)


ids = results.get(
    "ids",
    []
)

documents = results.get(
    "documents",
    []
)

metadatas = results.get(
    "metadatas",
    []
)


print(
    "Total chunks for document 1:",
    len(ids)
)


for index in range(
    min(3, len(ids))
):

    print(
        f"\n--- CHUNK {index + 1} ---"
    )

    print(
        "ID:",
        ids[index]
    )

    print(
        "Metadata:",
        metadatas[index]
    )

    print(
        "Content:"
    )

    print(
        documents[index][:300]
    )