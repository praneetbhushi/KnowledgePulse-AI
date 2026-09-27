import chromadb


class VectorStoreService:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="knowledgepulse_documents"
            )
        )

        self.document_collection = (
            self.client.get_or_create_collection(
                name="knowledgepulse_document_embeddings"
            )
        )

    def add_document_chunks(
        self,
        document_id: int,
        chunks: list,
        embeddings: list,
    ):

        if len(chunks) != len(embeddings):
    
            raise ValueError(
                "Chunks and embeddings count do not match."
            )

        ids = []

        documents = []

        metadatas = []

        unique = set()

        for index, (chunk, embedding) in enumerate(

            zip(chunks, embeddings)

        ):

            text = chunk["text"].strip()

            normalized = text.lower()

            if normalized in unique:
                continue

            unique.add(normalized)

            ids.append(
                f"doc_{document_id}_chunk_{index}"
            )

            documents.append(text)

            metadatas.append(

                {
                    "document_id": document_id,
                    "chunk_index": index,
                    "page": chunk["page"],
                    "section": chunk["section"],
                    "word_count": chunk["word_count"],
                }

            )

        self.collection.upsert(

            ids=ids,

            documents=documents,

            embeddings=embeddings[:len(ids)],

            metadatas=metadatas,

        )

        print("\n========== CHROMADB ==========\n")

        print(
            f"Stored {len(ids)} chunks."
        )

    def search(
        self,
        query_embedding,
        n_results=5,
    ):

        return self.collection.query(

            query_embeddings=[
                query_embedding
            ],

            n_results=n_results,

        )

    def get_collection_count(self):

        return self.collection.count()


vector_store_service = VectorStoreService()