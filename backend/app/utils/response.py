<<<<<<< HEAD
from __future__ import annotations

from typing import Any, Optional

from fastapi.responses import JSONResponse


def success_response(
    data: Any = None,
    message: str = "success",
    code: int = 0,
    status_code: int = 200,
) -> JSONResponse:
    payload = {
        "code": code,
        "message": message,
        "data": data,
    }
    return JSONResponse(status_code=status_code, content=payload)


def error_response(
    message: str = "error",
    code: int = 4000,
    data: Optional[Any] = None,
    status_code: int = 400,
) -> JSONResponse:
    payload = {
        "code": code,
        "message": message,
        "data": data,
    }
    return JSONResponse(status_code=status_code, content=payload)
=======
from __future__ import annotations

from typing import Any, Optional

from fastapi.responses import JSONResponse


def success_response(
    data: Any = None,
    message: str = "success",
    code: int = 0,
    status_code: int = 200,
) -> JSONResponse:
    payload = {
        "code": code,
        "message": message,
        "data": data,
    }
    return JSONResponse(status_code=status_code, content=payload)


def error_response(
    message: str = "error",
    code: int = 4000,
    data: Optional[Any] = None,
    status_code: int = 400,
) -> JSONResponse:
    payload = {
        "code": code,
        "message": message,
        "data": data,
    }
    return JSONResponse(status_code=status_code, content=payload)
>>>>>>> 98bf8e49 (update)
