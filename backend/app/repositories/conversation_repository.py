from sqlalchemy.orm import Session

from app.db.models.conversation import (
    Conversation
)


class ConversationRepository:

    def create(
        self,
        db: Session,
        user_id: int,
        title: str
    ):

        conversation = Conversation(
            user_id=user_id,
            title=title
        )

        db.add(
            conversation
        )

        db.commit()

        db.refresh(
            conversation
        )

        return conversation


    def get_by_id(
        self,
        db: Session,
        conversation_id: int
    ):

        return (
            db.query(
                Conversation
            )
            .filter(
                Conversation.id
                == conversation_id
            )
            .first()
        )


conversation_repository = (
    ConversationRepository()
)