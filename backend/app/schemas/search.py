from pydantic import BaseModel, Field
from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Semantic search query"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20
    )

    max_distance: float | None = Field(
        default=None,
        ge=0,
        description="Maximum vector distance allowed"
    )
    
    document_id: int | None = Field(
        default=None,
        ge=1
    )


class SearchResult(BaseModel):
    document_id: int
    document_name: str
    chunk_index: int
    content: str
    distance: float


class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: list[SearchResult]