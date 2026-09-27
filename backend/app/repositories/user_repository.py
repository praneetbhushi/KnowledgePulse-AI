from sqlalchemy.orm import Session

from app.db.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):

    def __init__(self):
        super().__init__(User)

    def get_by_email(
        self,
        db: Session,
        email: str
    ):
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )
    def get_all(
    self,
    db: Session,
    skip: int = 0,
    limit: int = 100
    ):
        return (
        db.query(self.model)
        .offset(skip)
        .limit(limit)
        .all()
        )


user_repository = UserRepository()