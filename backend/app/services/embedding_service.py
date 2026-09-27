from sentence_transformers import SentenceTransformer
import time


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            local_files_only=True
        )

    def generate_embedding(self, text: str) -> list[float]:
        """
        Generate embedding for a single text.
        """

        start = time.time()

        embedding = self.model.encode(
            text,
            convert_to_numpy=True
        )

        print(
            f"Embedding Time: {time.time() - start:.2f}s"
        )

        return embedding.tolist()

    def generate_embeddings(
        self,
        texts: list[str]
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        if not texts:
            return []

        start = time.time()

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )

        print(
            f"Batch Embedding Time: "
            f"{time.time() - start:.2f}s"
        )

        return embeddings.tolist()


# Singleton instance
embedding_service = EmbeddingService()


if __name__ == "__main__":

    sample_text = (
        "KnowledgePulse AI is an Enterprise "
        "Knowledge Health and Intelligence Platform."
    )

    vector = embedding_service.generate_embedding(
        sample_text
    )

    print("Embedding Length:", len(vector))

    print("First 10 Values:")
    print(vector[:10])