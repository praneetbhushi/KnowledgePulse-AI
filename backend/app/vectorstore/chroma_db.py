import chromadb


class ChromaDBService:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="app/vectorstore/chroma_data"
        )

        self.collection = self.client.get_or_create_collection(
            name="knowledgepulse_documents"
        )

    def add_documents(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:

        if not (
            len(ids)
            == len(documents)
            == len(embeddings)
            == len(metadatas)
        ):
            raise ValueError(
                "All input lists must have the same length."
            )

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 5,
    ):

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

    def count(self) -> int:

        return self.collection.count()

    def delete_document(
        self,
        ids: list[str],
    ):

        self.collection.delete(ids=ids)

    def reset_database(self):

        all_data = self.collection.get()

        if all_data["ids"]:
            self.collection.delete(ids=all_data["ids"])

    def get_all_documents(self):

        return self.collection.get()


chroma_db_service = ChromaDBService()