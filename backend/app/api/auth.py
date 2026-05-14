from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.deps import get_current_user
from app.core.exceptions import AppException
from app.core.security import (
    build_token_payload,
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.schemas.auth import ChangePasswordRequest, LoginRequest
from app.services.audit_log_service import audit_log_service
from app.storage.repositories import users_repo
from app.utils.response import success_response

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(payload: LoginRequest):
    user = users_repo.get_by_username(payload.username)
    if user is None:
        audit_log_service.record(
            module="auth",
            action="login",
            result="failed",
            message="用户名或密码错误",
            operator_username=payload.username,
            target_type="user",
            target_name=payload.username,
        )
        raise AppException(message="用户名或密码错误", code=4001, status_code=400)

    if not user.get("is_active", True):
        audit_log_service.record(
            module="auth",
            action="login",
            result="failed",
            message="账号已被禁用",
            operator=user,
            target_type="user",
            target_id=int(user["id"]),
            target_name=user.get("username"),
        )
        raise AppException(message="账号已被禁用", code=4002, status_code=403)

    password_hash = user.get("password_hash", "")
    if not verify_password(payload.password, password_hash):
        audit_log_service.record(
            module="auth",
            action="login",
            result="failed",
            message="用户名或密码错误",
            operator=user,
            target_type="user",
            target_id=int(user["id"]),
            target_name=user.get("username"),
        )
        raise AppException(message="用户名或密码错误", code=4001, status_code=400)

    access_token = create_access_token(build_token_payload(user))
    audit_log_service.record(
        module="auth",
        action="login",
        result="success",
        message="登录成功",
        operator=user,
        target_type="user",
        target_id=int(user["id"]),
        target_name=user.get("username"),
    )

    return success_response(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in_minutes": ACCESS_TOKEN_EXPIRE_MINUTES,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
                "student_id": user.get("student_id"),
                "is_active": user.get("is_active", True),
                "created_at": user.get("created_at"),
            },
        },
        message="登录成功",
    )


@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return success_response(
        data={
            "id": current_user["id"],
            "username": current_user["username"],
            "role": current_user["role"],
            "student_id": current_user.get("student_id"),
            "is_active": current_user.get("is_active", True),
            "created_at": current_user.get("created_at"),
        }
    )


@router.post("/change-password")
async def change_password(
    payload: ChangePasswordRequest,
    current_user=Depends(get_current_user),
):
    if payload.current_password == payload.new_password:
        audit_log_service.record(
            operator=current_user,
            module="auth",
            action="change_password",
            result="failed",
            message="新密码不能与当前密码相同",
            target_type="user",
            target_id=int(current_user["id"]),
            target_name=current_user.get("username"),
        )
        raise AppException(message="新密码不能与当前密码相同", code=4003, status_code=400)

    password_hash = current_user.get("password_hash", "")
    if not verify_password(payload.current_password, password_hash):
        audit_log_service.record(
            operator=current_user,
            module="auth",
            action="change_password",
            result="failed",
            message="当前密码错误",
            target_type="user",
            target_id=int(current_user["id"]),
            target_name=current_user.get("username"),
        )
        raise AppException(message="当前密码错误", code=4004, status_code=400)

    updated_user = users_repo.update(
        int(current_user["id"]),
        {
            "password_hash": get_password_hash(payload.new_password),
        },
    )
    if updated_user is None:
        audit_log_service.record(
            operator=current_user,
            module="auth",
            action="change_password",
            result="failed",
            message="密码修改失败",
            target_type="user",
            target_id=int(current_user["id"]),
            target_name=current_user.get("username"),
        )
        raise AppException(message="密码修改失败", code=5001, status_code=500)

    audit_log_service.record(
        operator=current_user,
        module="auth",
        action="change_password",
        result="success",
        message="密码修改成功",
        target_type="user",
        target_id=int(updated_user["id"]),
        target_name=updated_user.get("username"),
    )

    return success_response(
        data={
            "user_id": updated_user["id"],
            "username": updated_user["username"],
        },
        message="密码修改成功",
    )


@router.post("/logout")
async def logout(current_user=Depends(get_current_user)):
    audit_log_service.record(
        operator=current_user,
        module="auth",
        action="logout",
        result="success",
        message="退出登录",
        target_type="user",
        target_id=int(current_user["id"]),
        target_name=current_user.get("username"),
    )
    return success_response(
        data={
            "user_id": current_user["id"],
            "logout_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        message="退出登录成功",
    )
