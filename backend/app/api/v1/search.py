from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.api.deps import (
    get_db
)

from app.core.dependencies import (
    get_current_user
)

from app.schemas.search import (
    SearchRequest,
    SearchResponse
)

from app.services.search_service import (
    search_service
)

from app.repositories.search_query_repository import (
    search_query_repository
)

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.post(
    "",
    response_model=SearchResponse
)
def semantic_search(
    search_data: SearchRequest,

    db: Session = Depends(
        get_db
    ),

    current_user=Depends(
        get_current_user
    )
):

    # ---------------------------------
    # 1. Perform semantic search
    # ---------------------------------

    search_response = search_service.search(
        db=db,
        query=search_data.query,
        top_k=search_data.top_k
    )

    results = search_response.get(
        "results",
        []
    )


    # ---------------------------------
    # 2. Find best semantic distance
    # ---------------------------------

    best_distance = None

    if results:

        distances = [
            result["distance"]
            for result in results
            if result.get("distance")
            is not None
        ]

        if distances:
            best_distance = min(
                distances
            )


    # ---------------------------------
    # 3. Save search analytics
    # ---------------------------------

    search_query_repository.create(
        db=db,
        query=search_data.query,
        user_id=current_user.id,
        result_count=len(results),
        best_distance=best_distance
    )


    # ---------------------------------
    # 4. Return search results
    # ---------------------------------

    return {
        "query":
            search_data.query,

        "total_results":
            len(results),

        "results":
            results
    }