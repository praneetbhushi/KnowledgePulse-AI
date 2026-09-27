from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.dependencies import get_current_user
from app.services.dashboard_analytics_service import (
    dashboard_analytics_service
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return dashboard_analytics_service.get_dashboard_summary(
        db=db
    )