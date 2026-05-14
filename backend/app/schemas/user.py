from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=6, max_length=128)
    role: str = Field(default="teacher", min_length=1, max_length=32)
    is_active: bool = True


class UserUpdateRequest(BaseModel):
    username: Optional[str] = Field(default=None, min_length=1, max_length=64)
    is_active: Optional[bool] = None


class UserResetPasswordRequest(BaseModel):
    password: str = Field(default="123456", min_length=1, max_length=128)
