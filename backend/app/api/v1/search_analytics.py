from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    Query,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.core.dependencies import (
    get_current_user
)

from app.services.search_analytics_service import (
    search_analytics_service
)


router = APIRouter(
    prefix="/search-analytics",
    tags=["Search Analytics"]
)


@router.get("")
def get_search_analytics(
    start_date: datetime | None = Query(default=None),
    end_date: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # Validate date range
    if (
        start_date is not None
        and end_date is not None
        and start_date > end_date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date cannot be later than end_date."
        )

    analytics = (
        search_analytics_service.get_analytics(
            db=db,
            start_date=start_date,
            end_date=end_date
        )
    )

    return analytics