from sqlalchemy.orm import Session

from app.db.models.chat_message import (
    ChatMessage
)


class ChatMessageRepository:

    def create(
        self,
        db: Session,
        conversation_id: int,
        role: str,
        content: str
    ):

        message = ChatMessage(
            conversation_id=conversation_id,
            role=role,
            content=content
        )

        db.add(
            message
        )

        db.commit()

        db.refresh(
            message
        )

        return message


    def get_conversation_messages(
        self,
        db: Session,
        conversation_id: int,
        limit: int = 10
    ):

        messages = (
            db.query(
                ChatMessage
            )
            .filter(
                ChatMessage.conversation_id
                == conversation_id
            )
            .order_by(
                ChatMessage.created_at.desc()
            )
            .limit(
                limit
            )
            .all()
        )

        return list(
            reversed(messages)
        )


chat_message_repository = (
    ChatMessageRepository()
)