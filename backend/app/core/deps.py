<<<<<<< HEAD
from __future__ import annotations

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.core.exceptions import AppException
from app.core.security import decode_access_token, is_student, is_teacher
from app.storage.repositories import users_repo

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if credentials is None or not credentials.credentials:
        raise AppException(message="未登录或缺少访问令牌", code=4010, status_code=401)

    token = credentials.credentials
    try:
        payload = decode_access_token(token)
    except JWTError:
        raise AppException(message="访问令牌无效或已过期", code=4011, status_code=401)

    user_id = payload.get("user_id")
    if user_id is None:
        raise AppException(message="访问令牌缺少用户信息", code=4012, status_code=401)

    user = users_repo.get_by_id(int(user_id))
    if user is None:
        raise AppException(message="用户不存在", code=4013, status_code=401)

    if not user.get("is_active", True):
        raise AppException(message="用户已被禁用", code=4014, status_code=403)

    return user


def require_teacher(current_user=Depends(get_current_user)):
    if not is_teacher(current_user):
        raise AppException(message="需要教师权限", code=4031, status_code=403)
    return current_user


def require_student(current_user=Depends(get_current_user)):
    if not is_student(current_user):
        raise AppException(message="需要学生权限", code=4032, status_code=403)
    return current_user
=======
from __future__ import annotations

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.core.exceptions import AppException
from app.core.security import decode_access_token, is_student, is_teacher
from app.storage.repositories import users_repo

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if credentials is None or not credentials.credentials:
        raise AppException(message="未登录或缺少访问令牌", code=4010, status_code=401)

    token = credentials.credentials
    try:
        payload = decode_access_token(token)
    except JWTError:
        raise AppException(message="访问令牌无效或已过期", code=4011, status_code=401)

    user_id = payload.get("user_id")
    if user_id is None:
        raise AppException(message="访问令牌缺少用户信息", code=4012, status_code=401)

    user = users_repo.get_by_id(int(user_id))
    if user is None:
        raise AppException(message="用户不存在", code=4013, status_code=401)

    if not user.get("is_active", True):
        raise AppException(message="用户已被禁用", code=4014, status_code=403)

    return user


def require_teacher(current_user=Depends(get_current_user)):
    if not is_teacher(current_user):
        raise AppException(message="需要教师权限", code=4031, status_code=403)
    return current_user


def require_student(current_user=Depends(get_current_user)):
    if not is_student(current_user):
        raise AppException(message="需要学生权限", code=4032, status_code=403)
    return current_user
>>>>>>> 98bf8e49 (update)
