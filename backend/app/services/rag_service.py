from sqlalchemy.orm import Session
import time

from app.services.search_service import search_service
from app.services.prompt_service import prompt_service
from app.services.llm_service import llm_service
from app.db.models.search_query import SearchQuery


class RAGService:

    # ============================================================
    # RETRIEVE CONTEXT
    # ============================================================

    def retrieve_context(
        self,
        db: Session,
        question: str,
        top_k: int = 3,
        max_distance: float | None = None,
        document_id: int | None = None,
    ):

        # --------------------------------------------------------
        # Semantic Search
        # --------------------------------------------------------

        search_data = search_service.search(
            db=db,
            query=question,
            top_k=top_k,
            max_distance=max_distance,
            document_id=document_id,
        )

        # search_service now returns:
        #
        # {
        #     "results": [...],
        #     "search_time": ...,
        #     "best_distance": ...
        # }

        results = search_data.get(
            "results",
            []
        )

        search_time = search_data.get(
            "search_time",
            0.0
        )

        best_distance = search_data.get(
            "best_distance"
        )

        if not results:

            return {
                "context": "",
                "sources": [],
                "search_time": search_time,
                "best_distance": best_distance,
            }

        context_parts = []
        sources = []

        # --------------------------------------------------------
        # Process Retrieved Chunks
        # --------------------------------------------------------

        for result in results:

            document_name = (
                result.get("document_name")
                or result.get("filename")
                or "Unknown Document"
            )

            chunk_index = (
                result.get("chunk_index")
                if result.get("chunk_index") is not None
                else result.get("chunk", 0)
            )

            content = (
                result.get("content")
                or result.get("text")
                or ""
            )

            distance = result.get(
                "distance"
            )

            result_document_id = result.get(
                "document_id"
            )

            # ----------------------------------------------------
            # Build context for LLM
            # ----------------------------------------------------

            context_parts.append(
                            f"""
            Document: {document_name}
            Chunk: {chunk_index}
            Content:
            {content}
            """.strip()
            )

            # ----------------------------------------------------
            # Build source information
            # ----------------------------------------------------

            sources.append(
                {
                    "document_id": result_document_id,
                    "document_name": document_name,
                    "chunk_index": chunk_index,
                    "distance": distance,
                    "content": content,
                }
            )

        # --------------------------------------------------------
        # Final Context
        # --------------------------------------------------------

        context = "\n\n".join(
            context_parts
        )

        return {
            "context": context,
            "sources": sources,
            "search_time": search_time,
            "best_distance": best_distance,
        }

    # ============================================================
    # ANSWER QUESTION
    # ============================================================

    def answer_question(
        self,
        db: Session,
        question: str,
        top_k: int = 3,
        max_distance: float | None = None,
        document_id: int | None = None,
        conversation_history: str = "",
        user_id: int = 1,
    ):

        total_start = time.time()

        question = question.strip()

        # --------------------------------------------------------
        # Validate question
        # --------------------------------------------------------

        if not question:

            return {
                "answer": "Please provide a valid question.",
                "sources": [],
            }

        # --------------------------------------------------------
        # Retrieve Context
        # --------------------------------------------------------

        rag_data = self.retrieve_context(
            db=db,
            question=question,
            top_k=top_k,
            max_distance=max_distance,
            document_id=document_id,
        )

        context = rag_data["context"]

        sources = rag_data["sources"]

        search_time = rag_data.get(
            "search_time",
            0.0
        )

        best_distance = rag_data.get(
            "best_distance"
        )

        # --------------------------------------------------------
        # No relevant documents
        # --------------------------------------------------------

        if not sources:

            total_rag_time = (
                time.time() - total_start
            )

            # Save unsuccessful search
            search_query = SearchQuery(
                query=question,
                user_id=user_id,
                result_count=0,
                best_distance=best_distance,
                search_time=search_time,
                llm_time=0.0,
                total_rag_time=total_rag_time,
                was_answered=False,
            )

            db.add(search_query)
            db.commit()

            print(
                "\n========== SEARCH ANALYTICS =========="
            )

            print(
                f"Search Time     : {search_time:.2f}s"
            )

            print(
                f"LLM Time        : 0.00s"
            )

            print(
                f"Total RAG Time  : "
                f"{total_rag_time:.2f}s"
            )

            print(
                "Was Answered    : False"
            )

            print(
                "=======================================\n"
            )

            return {
                "answer": (
                    "I could not find enough information "
                    "in the available documents."
                ),
                "sources": [],
            }

        # --------------------------------------------------------
        # Build RAG Prompt
        # --------------------------------------------------------

        prompt = prompt_service.build_rag_prompt(
            question=question,
            context=context,
            conversation_history=conversation_history,
        )

        print(
            "\n========== PROMPT ==========\n"
        )

        print(prompt)

        # --------------------------------------------------------
        # Generate Answer using LLM
        # --------------------------------------------------------

        llm_start = time.time()

        answer = llm_service.generate_answer(
            prompt
        )

        llm_time = (
            time.time() - llm_start
        )

        print(
            f"\nLLM Time : "
            f"{llm_time:.2f}s"
        )

        # --------------------------------------------------------
        # Determine whether answer was generated
        # --------------------------------------------------------

        was_answered = bool(
            answer and answer.strip()
        )

        # --------------------------------------------------------
        # Remove Duplicate Sources
        # --------------------------------------------------------

        final_sources = []

        seen = set()

        for source in sources:

            key = (
                source.get("document_id"),
                source.get("chunk_index"),
            )

            if key in seen:
                continue

            seen.add(key)

            final_sources.append(
                {
                    "document_id":
                        source.get("document_id"),

                    "document_name":
                        source.get("document_name"),

                    "chunk_index":
                        source.get("chunk_index"),
                }
            )

        # --------------------------------------------------------
        # Total RAG Time
        # --------------------------------------------------------

        total_rag_time = (
            time.time() - total_start
        )

        print(
            f"\nTotal RAG Time : "
            f"{total_rag_time:.2f}s"
        )

        # --------------------------------------------------------
        # SAVE SEARCH ANALYTICS
        # --------------------------------------------------------

        search_query = SearchQuery(

            query=question,

            user_id=user_id,

            result_count=len(sources),

            best_distance=best_distance,

            search_time=search_time,

            llm_time=llm_time,

            total_rag_time=total_rag_time,

            was_answered=was_answered,
        )

        db.add(search_query)

        db.commit()

        print(
            "\n========== SEARCH ANALYTICS =========="
        )

        print(
            f"Query           : {question}"
        )

        print(
            f"Results         : {len(sources)}"
        )

        print(
            f"Best Distance   : {best_distance}"
        )

        print(
            f"Search Time     : {search_time:.2f}s"
        )

        print(
            f"LLM Time        : {llm_time:.2f}s"
        )

        print(
            f"Total RAG Time  : "
            f"{total_rag_time:.2f}s"
        )

        print(
            f"Was Answered    : {was_answered}"
        )

        print(
            "=======================================\n"
        )

        # --------------------------------------------------------
        # Final API Response
        # --------------------------------------------------------

        return {
            "answer": answer,
            "sources": final_sources,
        }


# ================================================================
# SINGLE RAG SERVICE INSTANCE
# ================================================================

rag_service = RAGService()