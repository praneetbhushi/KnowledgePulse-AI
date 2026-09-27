from sqlalchemy.orm import Session
import time
import re

from app.services.embedding_service import embedding_service
from app.services.vector_store_service import vector_store_service
from app.repositories.document_repository import document_repository
from app.vectorstore.chroma_db import chroma_db_service


class SearchService:

    def _keyword_score(
        self,
        query: str,
        content: str,
    ) -> float:

        stop_words = {
            "what",
            "is",
            "are",
            "the",
            "a",
            "an",
            "in",
            "on",
            "of",
            "to",
            "for",
            "and",
            "or",
            "this",
            "that",
            "document",
            "mentioned",
            "tell",
            "me",
            "about",
        }

        query_words = set(
            re.findall(
                r"\b[a-zA-Z][a-zA-Z0-9+#.-]*\b",
                query.lower(),
            )
        )

        query_words = {
            word
            for word in query_words
            if word not in stop_words
        }

        if not query_words:
            return 0.0

        content_words = set(
            re.findall(
                r"\b[a-zA-Z][a-zA-Z0-9+#.-]*\b",
                content.lower(),
            )
        )

        matched_words = (
            query_words & content_words
        )

        return len(matched_words) / len(query_words)

    def search(
        self,
        db: Session,
        query: str,
        top_k: int = 5,
        max_distance: float | None = None,
        document_id: int | None = None,
    ):

        total_start = time.time()

        # =====================================================
        # STEP 1: Generate query embedding
        # =====================================================

        embedding_start = time.time()

        query_embedding = embedding_service.generate_embedding(
            query
        )

        print(
            f"Embedding Time : "
            f"{time.time() - embedding_start:.2f}s"
        )

        # =====================================================
        # STEP 2: Search ChromaDB
        # =====================================================

        # Retrieve more candidates than final top_k
        candidate_count = max(top_k * 4, 12)

        query_args = {
            "query_embeddings": [query_embedding],
            "n_results": candidate_count,
        }

        if document_id is not None:

            query_args["where"] = {
                "document_id": document_id
            }

        chroma_start = time.time()

        results = vector_store_service.collection.query(
            **query_args
        )

        print(
            f"Chroma Search : "
            f"{time.time() - chroma_start:.2f}s"
        )

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

        if not documents:
            print("No ChromaDB results found.")
            return {
            "results": [],
            "search_time": time.time() - total_start,
            "best_distance": None,
        }

        # =====================================================
        # STEP 3: Cache PostgreSQL documents
        # =====================================================

        document_cache = {}

        search_results = []

        for content, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):

            if metadata is None:
                continue

            result_document_id = metadata.get(
                "document_id"
            )

            if result_document_id is None:
                continue

            distance = float(distance)

            # ---------------------------------------------
            # Load document only once
            # ---------------------------------------------

            if result_document_id not in document_cache:

                document_cache[
                    result_document_id
                ] = document_repository.get(
                    db,
                    result_document_id
                )

            db_document = document_cache[
                result_document_id
            ]

            if db_document is None:
                continue

            chunk_index = metadata.get(
                "chunk_index",
                0
            )

            result = {

                "document_id":
                    result_document_id,

                "document_name":
                    db_document.original_filename,

                "chunk_index":
                    chunk_index,

                "content":
                    content,

                "distance":
                    distance,
            }

            search_results.append(result)

        # =====================================================
        # STEP 4: Calculate hybrid relevance
        # =====================================================

        for result in search_results:

            result["keyword_score"] = self._keyword_score(
                query=query,
                content=result["content"],
            )
        # =====================================================
        # STEP 4B: Sort by semantic + keyword relevance
        # =====================================================
        if not search_results:
            print("No valid search results after document filtering.")
            return {
                "results": [],
                "search_time": time.time() - total_start,
                "best_distance": None,
            }

        best_distance = min(
            result["distance"]
            for result in search_results
        )

        for result in search_results:

            distance = result["distance"]

            # Convert distance into a semantic score.
            # Lower distance = higher semantic relevance.
            semantic_score = (
                1 / (1 + distance)
            )

            keyword_score = result["keyword_score"]

            # Semantic similarity remains the main signal.
            # Keyword relevance provides an additional signal
            # when the query contains useful matching terms.
            result["relevance_score"] = (
                semantic_score * 0.70
                + keyword_score * 0.30
            )

        search_results.sort(
            key=lambda x: x["relevance_score"],
            reverse=True,
        )

        # =====================================================
        # STEP 5: Distance filtering
        # =====================================================

        if not search_results:
            return {
            "results": [],
            "search_time": time.time() - total_start,
            "best_distance": None,
        }

        best_distance = search_results[0]["distance"]

        if max_distance is not None:
    
            threshold = max_distance

        else:

            # Keep results close to the best match while also
            # rejecting globally weak semantic matches.
            threshold = min(
                best_distance + 0.08,
                0.75,
            )

        filtered_results = [

            result

            for result in search_results

            if result["distance"] <= threshold

        ]

        # =====================================================
        # STEP 6: Select final relevant chunks
        # =====================================================

        final_results = []

        seen_chunks = set()

        for result in filtered_results:

            chunk_key = (
                result["document_id"],
                result["chunk_index"],
            )

            if chunk_key in seen_chunks:
                continue

            seen_chunks.add(chunk_key)

            final_results.append(result)

            if len(final_results) >= top_k:
                break

        print(
            "\n========== FINAL RAG CHUNKS ==========\n"
        )

        for result in final_results:

            print(
                f"{result['document_name']} "
                f"| Chunk {result['chunk_index']} "
                f"| Distance {result['distance']:.3f} "
                f"| Keyword {result.get('keyword_score', 0):.3f} "
                f"| Relevance {result.get('relevance_score', 0):.3f}"
            )

            print(
                result["content"][:250]
            )

            print("-" * 70)

        search_time = time.time() - total_start

        print(
            f"\nTotal Search Time : "
            f"{search_time:.2f}s"
        )

        return {
            "results": final_results,
            "search_time": search_time,
            "best_distance": (
                final_results[0]["distance"]
                if final_results
                else None
            ),
        }

    # --------------------------------------------

    def semantic_search(

        self,

        query: str,

        top_k: int = 5,

    ):

        query_embedding = (
            embedding_service.generate_embedding(
                query
            )
        )

        results = chroma_db_service.search(

            query_embedding=query_embedding,

            n_results=max(top_k * 3, 20),

        )

        response = []

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

        for document, metadata, distance in zip(

            documents,

            metadatas,

            distances,

        ):

            response.append(

                {

                    "text": document,

                    "metadata": metadata,

                    "distance": distance,

                }

            )

        return response


search_service = SearchService()