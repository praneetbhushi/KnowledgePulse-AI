from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.search import (
    SearchRequest,
    SearchResponse,
    SearchResult,
)

from app.services.search_service import (
    search_service,
)


router = APIRouter()


@router.post(
    "/semantic-search",
    response_model=SearchResponse,
)
def semantic_search(
    request: SearchRequest,
    db: Session = Depends(get_db),
):

    search_data = search_service.search(
        db=db,
        query=request.query,
        top_k=request.top_k,
    )

    results = search_data["results"]

    return SearchResponse(
        query=request.query,
        total_results=len(results),
        results=[
            SearchResult(
                text=result["content"],
                metadata={
                    "document_id": result["document_id"],
                    "document_name": result["document_name"],
                    "chunk_index": result["chunk_index"],
                },
                distance=result["distance"],
            )
            for result in results
        ],
    )