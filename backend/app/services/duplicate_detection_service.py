from app.services.embedding_service import (
    embedding_service
)

from app.services.vector_store_service import (
    vector_store_service
)


class DuplicateDetectionService:

    # ChromaDB distance threshold.
    # Smaller distance means greater similarity.
    DUPLICATE_DISTANCE_THRESHOLD = 0.15


    def detect_duplicate(
        self,
        text: str
    ):

        # ---------------------------------
        # STEP 1: Check empty text
        # ---------------------------------

        if not text or not text.strip():

            return {
                "is_duplicate": False,
                "duplicate_of_document_id": None,
                "similarity": None,
                "embedding": None
            }


        # ---------------------------------
        # STEP 2: Select document text
        #
        # We use a portion of the cleaned
        # document to create one embedding.
        # ---------------------------------

        document_text = text[:5000]


        # ---------------------------------
        # STEP 3: Generate one embedding
        # for the document
        # ---------------------------------

        document_embedding = (
            embedding_service.generate_embedding(
                document_text
            )
        )


        # ---------------------------------
        # STEP 4: Get duplicate-detection
        # ChromaDB collection
        # ---------------------------------

        collection = (
            vector_store_service
            .document_collection
        )


        # ---------------------------------
        # STEP 5: First document case
        #
        # If no document embeddings exist,
        # there is nothing to compare.
        # ---------------------------------

        if collection.count() == 0:

            return {
                "is_duplicate": False,
                "duplicate_of_document_id": None,
                "similarity": None,
                "embedding": document_embedding
            }


        # ---------------------------------
        # STEP 6: Search for the nearest
        # existing document
        # ---------------------------------

        results = collection.query(

            query_embeddings=[
                document_embedding
            ],

            n_results=1
        )


        # ---------------------------------
        # STEP 7: Extract IDs and distances
        # ---------------------------------

        ids = results.get(
            "ids",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]


        # ---------------------------------
        # STEP 8: Handle no results
        # ---------------------------------

        if not ids or not distances:

            return {
                "is_duplicate": False,
                "duplicate_of_document_id": None,
                "similarity": None,
                "embedding": document_embedding
            }


        # ---------------------------------
        # STEP 9: Get nearest document
        # ---------------------------------

        nearest_document_id = int(
            ids[0]
        )

        distance = float(
            distances[0]
        )


        # ---------------------------------
        # STEP 10: Calculate similarity
        # ---------------------------------

        similarity = 1.0 - distance


        # ---------------------------------
        # STEP 11: Determine duplicate
        # ---------------------------------

        is_duplicate = (
            distance
            <= self.DUPLICATE_DISTANCE_THRESHOLD
        )


        # ---------------------------------
        # STEP 12: Return detection result
        # ---------------------------------

        return {

            "is_duplicate":
                is_duplicate,

            "duplicate_of_document_id":
                nearest_document_id
                if is_duplicate
                else None,

            "similarity":
                round(
                    similarity,
                    4
                ),

            "embedding":
                document_embedding
        }


    def store_document_embedding(
        self,
        document_id: int,
        embedding
    ):

        # ---------------------------------
        # STEP 13: Ignore missing embedding
        # ---------------------------------

        if embedding is None:
            return


        # ---------------------------------
        # STEP 14: Store one embedding
        # for this document in ChromaDB
        # ---------------------------------

        vector_store_service.document_collection.add(

            ids=[
                str(document_id)
            ],

            embeddings=[
                embedding
            ],

            metadatas=[
                {
                    "document_id":
                        document_id
                }
            ]
        )


# ---------------------------------
# Create service instance
# ---------------------------------

duplicate_detection_service = (
    DuplicateDetectionService()
)