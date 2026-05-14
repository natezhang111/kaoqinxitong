<<<<<<< HEAD
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Optional[Any] = None
=======
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Optional[Any] = None
>>>>>>> 98bf8e49 (update)
