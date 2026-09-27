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

from app.services.department_analytics_service import (
    department_analytics_service
)


router = APIRouter(
    prefix="/departments",
    tags=["Department Analytics"]
)


@router.get(
    "/{department_id}/analytics"
)
def get_department_analytics(
    department_id: int,

    db: Session = Depends(
        get_db
    ),

    current_user=Depends(
        get_current_user
    )
):

    # ---------------------------------
    # Get department analytics
    # ---------------------------------

    analytics = (
        department_analytics_service
        .get_department_analytics(
            db=db,
            department_id=department_id
        )
    )

    # ---------------------------------
    # Department not found
    # ---------------------------------

    if analytics is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found."
        )

    # ---------------------------------
    # Return analytics
    # ---------------------------------

    return analytics