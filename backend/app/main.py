from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import logger
from fastapi.staticfiles import StaticFiles
from app.core.exceptions.custom_exceptions import (
    UserNotFoundException,
    EmailAlreadyExistsException,
    DepartmentNotFoundException,
    RoleNotFoundException,
    KnowledgePulseException,
    InvalidFileTypeException,
    FileTooLargeException,
)

from app.core.exceptions.handlers import (
    user_not_found_handler,
    email_exists_handler,
    department_not_found_handler,
    role_not_found_handler,
    knowledgepulse_exception_handler,
    invalid_file_handler,
    file_too_large_handler,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("KnowledgePulse AI Starting...")
    yield
    logger.info("KnowledgePulse AI Shutting Down...")


app = FastAPI(
    title="KnowledgePulse AI",
    description="Enterprise Knowledge Health & Intelligence Platform",
    version="1.0.0",
)

# Exception Handlers
app.add_exception_handler(
    InvalidFileTypeException,
    invalid_file_handler,
)

app.add_exception_handler(
    FileTooLargeException,
    file_too_large_handler,
)

app.add_exception_handler(
    UserNotFoundException,
    user_not_found_handler,
)

app.add_exception_handler(
    EmailAlreadyExistsException,
    email_exists_handler,
)

app.add_exception_handler(
    DepartmentNotFoundException,
    department_not_found_handler,
)

app.add_exception_handler(
    RoleNotFoundException,
    role_not_found_handler,
)

app.add_exception_handler(
    KnowledgePulseException,
    knowledgepulse_exception_handler,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(
    api_router,
    prefix="/api/v1",
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)
# Root Endpoint
@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "Running",
        "message": "Welcome to KnowledgePulse AI 🚀",
    }