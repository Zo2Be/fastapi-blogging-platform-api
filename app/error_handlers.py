from typing import TYPE_CHECKING

from fastapi.responses import ORJSONResponse

from core.exceptions import NotFoundError, UnauthorizedError, ForbiddenError
from main import main_app

if TYPE_CHECKING:
    from fastapi import Request


@main_app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: "Request", exc: NotFoundError):
    return ORJSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        },
    )


@main_app.exception_handler(UnauthorizedError)
async def unauthorized_exception_handler(request: "Request", exc: UnauthorizedError):
    return ORJSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        },
    )


@main_app.exception_handler(ForbiddenError)
async def forbidden_exception_handler(request: "Request", exc: ForbiddenError):
    return ORJSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        },
    )
