from sqlalchemy.orm import Session

from app.db.models.user import User
from app.repositories.user_repository import user_repository
from app.core.security import get_password_hash

from app.core.exceptions.custom_exceptions import (
    EmailAlreadyExistsException,
    UserNotFoundException,
)


class UserService:

    def get_user(
        self,
        db: Session,
        user_id: int
    ):
        return user_repository.get(
            db,
            user_id
        )

    def get_all_users(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ):
        return user_repository.get_all(
            db,
            skip,
            limit
        )

    def create_user(
        self,
        db: Session,
        user
    ):
        existing_user = user_repository.get_by_email(
            db,
            user.email
        )

        if existing_user:
            raise EmailAlreadyExistsException(
                "Email already exists."
            )

        db_user = User(
            name=user.name,
            email=user.email,
            password=get_password_hash(
                user.password
            ),
            department_id=user.department_id,
            role_id=user.role_id
        )

        return user_repository.create(
            db,
            db_user
        )

    def update_user(
        self,
        db: Session,
        user_id: int,
        user
    ):
        db_user = user_repository.get(
            db,
            user_id
        )

        if db_user is None:
            raise UserNotFoundException(
                "User not found."
            )

        update_data = user.model_dump(
            exclude_unset=True
        )

        return user_repository.update(
            db,
            db_user,
            update_data
        )

    def delete_user(
        self,
        db: Session,
        user_id: int
    ):
        user = user_repository.delete(
            db,
            user_id
        )

        if user is None:
            raise UserNotFoundException(
                "User not found."
            )

        return user


user_service = UserService()