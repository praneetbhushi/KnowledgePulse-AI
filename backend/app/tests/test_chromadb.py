from app.services.embedding_service import embedding_service
from app.vectorstore.chroma_db import chroma_db_service

text = "KnowledgePulse AI is an enterprise knowledge platform."

embedding = embedding_service.generate_embedding(text)

chroma_db_service.add_documents(
    ids=["doc1"],
    documents=[text],
    embeddings=[embedding],
    metadatas=[
        {
            "source": "demo",
            "chunk": 1,
        }
    ],
)

print("Stored Documents:", chroma_db_service.count())

query = "knowledge management system"

query_embedding = embedding_service.generate_embedding(query)

results = chroma_db_service.search(query_embedding)

print(results["documents"])