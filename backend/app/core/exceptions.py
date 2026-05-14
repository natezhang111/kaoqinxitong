<<<<<<< HEAD
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.utils.response import error_response


class AppException(Exception):
    def __init__(
        self,
        message: str,
        code: int = 4000,
        status_code: int = 400,
        data=None,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        self.data = data
        super().__init__(message)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return error_response(
            message=exc.message,
            code=exc.code,
            data=exc.data,
            status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return error_response(
            message="请求参数校验失败",
            code=4220,
            data={"errors": exc.errors()},
            status_code=422,
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return error_response(
            message=exc.detail if isinstance(exc.detail, str) else "HTTP 请求错误",
            code=exc.status_code,
            data=None,
            status_code=exc.status_code,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return error_response(
            message="服务器内部错误",
            code=5000,
            data={"detail": str(exc)} if app.debug else None,
            status_code=500,
        )
=======
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.utils.response import error_response


class AppException(Exception):
    def __init__(
        self,
        message: str,
        code: int = 4000,
        status_code: int = 400,
        data=None,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        self.data = data
        super().__init__(message)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return error_response(
            message=exc.message,
            code=exc.code,
            data=exc.data,
            status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return error_response(
            message="请求参数校验失败",
            code=4220,
            data={"errors": exc.errors()},
            status_code=422,
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return error_response(
            message=exc.detail if isinstance(exc.detail, str) else "HTTP 请求错误",
            code=exc.status_code,
            data=None,
            status_code=exc.status_code,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return error_response(
            message="服务器内部错误",
            code=5000,
            data={"detail": str(exc)} if app.debug else None,
            status_code=500,
        )
>>>>>>> 98bf8e49 (update)
