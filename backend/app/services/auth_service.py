from sqlalchemy.orm import Session

from app.repositories.user_repository import user_repository
from app.core.security import (
    verify_password,
    create_access_token,
)


class AuthService:
    

    def authenticate_user(
        self,
        db: Session,
        email: str,
        password: str
    ):
        user = user_repository.get_by_email(
            db,
            email
        )

        if not user:
            return None

        if not verify_password(
            password,
            user.password
        ):
            return None

        return user

    def login(
        self,
        db: Session,
        email: str,
        password: str
    ):
        user = self.authenticate_user(
            db,
            email,
            password
        )

        if user is None:
            return None

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role.name
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }


auth_service = AuthService()