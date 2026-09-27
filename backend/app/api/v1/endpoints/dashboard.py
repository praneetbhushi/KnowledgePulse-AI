from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.dashboard_analytics_service import (
    dashboard_analytics_service
)

router = APIRouter()


@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db)
):

    return dashboard_analytics_service.get_dashboard_summary(
        db=db
    )