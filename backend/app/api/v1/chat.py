from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.core.dependencies import (
    get_current_user
)

from app.core.exceptions.custom_exceptions import (
    LLMServiceException,
    LLMUnavailableException
)

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.repositories.conversation_repository import (
    conversation_repository
)

from app.repositories.chat_message_repository import (
    chat_message_repository
)

from app.services.rag_service import (
    rag_service
)


router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)


@router.post(
    "/",
    response_model=ChatResponse
)
def chat(
    chat_data: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:

        # --------------------------------
        # 1. Get or create conversation
        # --------------------------------

        if chat_data.conversation_id is not None:

            conversation = (
                conversation_repository.get_by_id(
                    db=db,
                    conversation_id=chat_data.conversation_id
                )
            )

            # Make sure conversation exists
            # and belongs to current user
            if (
                conversation is None
                or conversation.user_id != current_user.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )

        else:

            # Use first question as conversation title
            title = chat_data.question[:100]

            conversation = (
                conversation_repository.create(
                    db=db,
                    user_id=current_user.id,
                    title=title
                )
            )


        # --------------------------------
        # 2. Load previous conversation
        # --------------------------------

        previous_messages = (
            chat_message_repository
            .get_conversation_messages(
                db=db,
                conversation_id=conversation.id,
                limit=10
            )
        )


        history_parts = []

        for message in previous_messages:

            history_parts.append(
                f"{message.role}: "
                f"{message.content}"
            )


        conversation_history = "\n".join(
            history_parts
        )


        # --------------------------------
        # 3. Save current user message
        # --------------------------------

        chat_message_repository.create(
            db=db,
            conversation_id=conversation.id,
            role="user",
            content=chat_data.question
        )


        # --------------------------------
        # 4. Generate RAG answer
        # --------------------------------

        rag_result = rag_service.answer_question(
            db=db,
            question=chat_data.question,
            top_k=chat_data.top_k,
            max_distance=chat_data.max_distance,
            document_id=chat_data.document_id,
            conversation_history=conversation_history,
            user_id=current_user.id,
        )


        # --------------------------------
        # 5. Save assistant response
        # --------------------------------

        chat_message_repository.create(
            db=db,
            conversation_id=conversation.id,
            role="assistant",
            content=rag_result["answer"]
        )


        # --------------------------------
        # 6. Return response
        # --------------------------------

        return {
            "question": chat_data.question,
            "answer": rag_result["answer"],
            "conversation_id": conversation.id,
            "sources": rag_result["sources"]
        }


    # --------------------------------
    # 7. Ollama unavailable
    # --------------------------------

    except Exception as e:
        import traceback

        traceback.print_exc()

        raise


    # --------------------------------
    # 8. LLM generation error
    # --------------------------------

    except Exception as e:
        import traceback

        traceback.print_exc()

        raise

    