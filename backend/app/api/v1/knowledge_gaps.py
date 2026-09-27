from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.dependencies import get_current_user

from app.services.knowledge_gap_service import (
    knowledge_gap_service
)


router = APIRouter(
    prefix="/knowledge-gaps",
    tags=["Knowledge Gaps"]
)


@router.get("")
def get_knowledge_gaps(
    limit: int = Query(
        default=100,
        ge=1,
        le=1000
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    knowledge_gaps = (
        knowledge_gap_service.get_knowledge_gaps(
            db=db,
            limit=limit
        )
    )

    return {
        "total_gaps": len(knowledge_gaps),
        "knowledge_gaps": knowledge_gaps
    }