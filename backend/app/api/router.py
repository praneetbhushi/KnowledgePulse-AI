from fastapi import APIRouter

from app.api.v1 import auth
from app.api.v1 import users
from app.api.v1 import search

from app.api.v1.endpoints import dashboard
from app.api.v1.endpoints import document_upload
from app.api.v1 import chat
from app.api.v1.endpoints import knowledge_health

from app.api.v1.endpoints.analytics import (
    router as analytics_router
)
from app.api.v1.endpoints.document_analytics import (
    router as document_analytics_router
)

from app.api.v1.endpoints.document_quality import (
    router as document_quality_router,
)

from app.api.v1.endpoints import document_intelligence

api_router = APIRouter()


api_router.include_router(
    analytics_router,
    prefix="/analytics",
    tags=["Analytics"],
)


api_router.include_router(
    knowledge_health.router,
    prefix="/knowledge-health",
    tags=["Knowledge Health"],
)


api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)


api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)


api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"],
)


api_router.include_router(
    document_upload.router,
    prefix="/documents",
    tags=["Documents"],
)


api_router.include_router(
    chat.router,
)


api_router.include_router(
    search.router,
    prefix="/search",
    tags=["Search"],
)

api_router.include_router(
    document_analytics_router,
    prefix="/document-analytics",
    tags=["Document Analytics"],
)

api_router.include_router(
    document_quality_router,
    prefix="/document-quality",
    tags=["Document Quality"],
)

api_router.include_router(
    document_intelligence.router,
    prefix="/documents/intelligence",
    tags=["Document Intelligence"],
)