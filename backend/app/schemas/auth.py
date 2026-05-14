<<<<<<< HEAD
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


=======
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


>>>>>>> 98bf8e49 (update)
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=1, max_length=128)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1, max_length=128)
    new_password: str = Field(..., min_length=6, max_length=128)


class TokenData(BaseModel):
    sub: str
    user_id: int
    username: str
    role: str
<<<<<<< HEAD


class LoginResponseData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
    user: dict


class UserInfo(BaseModel):
    id: int
    username: str
    role: str
    student_id: Optional[int] = None
    is_active: bool = True
    created_at: str
=======


class LoginResponseData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
    user: dict


class UserInfo(BaseModel):
    id: int
    username: str
    role: str
    student_id: Optional[int] = None
    is_active: bool = True
    created_at: str
>>>>>>> 98bf8e49 (update)
