from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import (
    require_admin,
    require_manager,
)

from app.schemas.user import (
    UserResponse,
    UserUpdate,
)

from app.services.user_service import (
    user_service,
)


router = APIRouter(
    tags=["Users"]
)


@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return user_service.get_all_users(db)


@router.get(
    "/me",
    response_model=UserResponse
)
def read_current_user(
    current_user=Depends(get_current_user),
):
    return current_user


@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_manager),
):
    return user_service.update_user(
        db,
        user_id,
        user
    )


@router.delete(
    "/{user_id}",
    response_model=UserResponse
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return user_service.delete_user(
        db,
        user_id
    )