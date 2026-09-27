from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions.custom_exceptions import (
    KnowledgePulseException,
    UserNotFoundException,
    EmailAlreadyExistsException,
    DepartmentNotFoundException,
    RoleNotFoundException,
    InvalidFileTypeException,
    FileTooLargeException,)

async def invalid_file_handler(
    request: Request,
    exc: InvalidFileTypeException,
):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": exc.message,
        },
    )


async def file_too_large_handler(
    request: Request,
    exc: FileTooLargeException,
):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": exc.message,
        },
    )

async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": exc.message,
        },
    )


async def email_exists_handler(
    request: Request,
    exc: EmailAlreadyExistsException,
):
    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "error": exc.message,
        },
    )


async def department_not_found_handler(
    request: Request,
    exc: DepartmentNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": exc.message,
        },
    )


async def role_not_found_handler(
    request: Request,
    exc: RoleNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": exc.message,
        },
    )


async def knowledgepulse_exception_handler(
    request: Request,
    exc: KnowledgePulseException,
):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": exc.message,
        },
    )