from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Query

from app.core.deps import require_teacher
from app.core.exceptions import AppException
from app.core.security import get_password_hash
from app.schemas.user import (
    UserCreateRequest,
    UserResetPasswordRequest,
    UserUpdateRequest,
)
from app.services.audit_log_service import audit_log_service
from app.storage.repositories import students_repo, users_repo
from app.utils.response import success_response

router = APIRouter(prefix="/users", tags=["users"])

DEFAULT_USER_PASSWORD = "123456"

PERMISSION_MATRIX = [
    {
        "role": "teacher",
        "label": "教师",
        "permissions": [
            "登录教师端",
            "学生信息管理",
            "学生账号绑定与重置密码",
            "实时考勤与记录导出",
            "安全测试管理",
            "合照识别与准确率评估",
            "情绪统计与报表查看",
            "用户管理与审计日志查看",
        ],
    },
    {
        "role": "student",
        "label": "学生",
        "permissions": [
            "登录学生端",
            "查看本人档案信息",
            "查看本人考勤记录",
            "查看本人活动与合照记录",
            "查看本人情绪记录",
            "修改本人登录密码",
        ],
    },
]


def _get_student_meta(student_id: Optional[int]) -> Optional[Dict[str, Any]]:
    if student_id is None:
        return None
    student = students_repo.get_by_id(int(student_id))
    if student is None:
        return None
    return {
        "id": student["id"],
        "student_no": student.get("student_no"),
        "name": student.get("name"),
        "class_name": student.get("class_name"),
        "is_active": student.get("is_active", True),
    }


def _serialize_user(user: Dict[str, Any]) -> Dict[str, Any]:
    student_meta = _get_student_meta(user.get("student_id"))
    linked_student = student_meta is not None
    return {
        "id": user["id"],
        "username": user.get("username"),
        "role": user.get("role"),
        "student_id": user.get("student_id"),
        "is_active": user.get("is_active", True),
        "created_at": user.get("created_at"),
        "linked_student": linked_student,
        "account_source": "student_binding" if linked_student else "standalone",
        "student": student_meta,
        "can_edit_username": not linked_student,
        "can_delete": not linked_student,
        "can_reset_password": True,
    }


def _ensure_username_available(username: str, exclude_user_id: Optional[int] = None) -> None:
    existing = users_repo.get_by_username(username)
    if existing is None:
        return
    if exclude_user_id is not None and int(existing["id"]) == exclude_user_id:
        return
    raise AppException(message="用户名已存在", code=4005, status_code=400)


def _count_active_teachers(exclude_user_id: Optional[int] = None) -> int:
    count = 0
    for item in users_repo.list_all():
        if item.get("role") != "teacher":
            continue
        if not item.get("is_active", True):
            continue
        if exclude_user_id is not None and int(item["id"]) == exclude_user_id:
            continue
        count += 1
    return count


@router.get("/permission-matrix")
async def permission_matrix(current_user=Depends(require_teacher)):
    return success_response(data=PERMISSION_MATRIX)


@router.get("")
async def list_users(
    keyword: Optional[str] = Query(default=None, description="按用户名搜索"),
    role: Optional[str] = Query(default=None, description="按角色筛选：teacher/student"),
    is_active: Optional[bool] = Query(default=None, description="按启用状态筛选"),
    current_user=Depends(require_teacher),
):
    rows = users_repo.query_users(keyword=keyword, role=role, is_active=is_active)
    rows.sort(key=lambda item: int(item.get("id", 0)), reverse=True)
    return success_response(data=[_serialize_user(item) for item in rows])


@router.get("/{user_id}")
async def get_user(user_id: int, current_user=Depends(require_teacher)):
    user = users_repo.get_by_id(user_id)
    if user is None:
        raise AppException(message="用户不存在", code=4042, status_code=404)
    return success_response(data=_serialize_user(user))


@router.post("")
async def create_user(payload: UserCreateRequest, current_user=Depends(require_teacher)):
    try:
        role = payload.role.strip().lower()
        if role != "teacher":
            raise AppException(
                message="当前用户管理页仅允许创建教师账号，学生账号请在学生管理页维护",
                code=4006,
                status_code=400,
            )

        username = payload.username.strip()
        _ensure_username_available(username)

        created = users_repo.create(
            {
                "username": username,
                "password_hash": get_password_hash(payload.password),
                "role": "teacher",
                "student_id": None,
                "is_active": payload.is_active,
                "created_at": audit_log_service.now_str(),
            }
        )

        audit_log_service.record(
            operator=current_user,
            module="user_management",
            action="create_user",
            result="success",
            message="创建用户成功",
            target_type="user",
            target_id=int(created["id"]),
            target_name=created["username"],
            detail={"role": created["role"], "is_active": created["is_active"]},
        )
        return success_response(data=_serialize_user(created), message="用户创建成功")
    except AppException as exc:
        audit_log_service.record(
            operator=current_user,
            module="user_management",
            action="create_user",
            result="failed",
            message=exc.message,
            target_type="user",
            target_name=payload.username,
            detail={"role": payload.role, "is_active": payload.is_active},
        )
        raise


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    payload: UserUpdateRequest,
    current_user=Depends(require_teacher),
):
    user = users_repo.get_by_id(user_id)
    if user is None:
        raise AppException(message="用户不存在", code=4042, status_code=404)

    try:
        updates = payload.model_dump(exclude_unset=True)
        if not updates:
            return success_response(data=_serialize_user(user), message="没有需要更新的字段")

        linked_student = user.get("student_id") is not None and _get_student_meta(user.get("student_id")) is not None
        if linked_student and "username" in updates:
            raise AppException(
                message="已绑定学生档案的账号用户名请在学生管理模块维护",
                code=4007,
                status_code=400,
            )

        if "username" in updates:
            updates["username"] = updates["username"].strip()
            _ensure_username_available(updates["username"], exclude_user_id=user_id)

        if "is_active" in updates:
            next_active = bool(updates["is_active"])
            if not next_active and int(user["id"]) == int(current_user["id"]):
                raise AppException(message="不能停用当前登录账号", code=4008, status_code=400)
            if (
                user.get("role") == "teacher"
                and user.get("is_active", True)
                and not next_active
                and _count_active_teachers(exclude_user_id=user_id) == 0
            ):
                raise AppException(message="系统至少需要保留一个启用中的教师账号", code=4009, status_code=400)

        updated = users_repo.update(user_id, updates)
        if updated is None:
            raise AppException(message="用户更新失败", code=5002, status_code=500)

        audit_log_service.record(
            operator=current_user,
            module="user_management",
            action="update_user",
            result="success",
            message="更新用户成功",
            target_type="user",
            target_id=user_id,
            target_name=updated["username"],
            detail={"updates": updates},
        )
        return success_response(data=_serialize_user(updated), message="用户更新成功")
    except AppException as exc:
        audit_log_service.record(
            operator=current_user,
            module="user_management",
            action="update_user",
            result="failed",
            message=exc.message,
            target_type="user",
            target_id=user_id,
            target_name=user.get("username"),
            detail={"updates": payload.model_dump(exclude_unset=True)},
        )
        raise


@router.post("/{user_id}/reset-password")
async def reset_user_password(
    user_id: int,
    payload: UserResetPasswordRequest,
    current_user=Depends(require_teacher),
):
    user = users_repo.get_by_id(user_id)
    if user is None:
        raise AppException(message="用户不存在", code=4042, status_code=404)

    try:
        updated = users_repo.update(
            user_id,
            {
                "password_hash": get_password_hash(payload.password),
            },
        )
        if updated is None:
            raise AppException(message="重置密码失败", code=5003, status_code=500)

        audit_log_service.record(
            operator=current_user,
            module="user_management",
            action="reset_password",
            result="success",
            message="重置用户密码成功",
            target_type="user",
            target_id=user_id,
            target_name=user.get("username"),
        )
        return success_response(
            data={
                "user_id": user_id,
                "username": user.get("username"),
                "reset_password": payload.password,
            },
            message="用户密码重置成功",
        )
    except AppException as exc:
        audit_log_service.record(
            operator=current_user,
            module="user_management",
            action="reset_password",
            result="failed",
            message=exc.message,
            target_type="user",
            target_id=user_id,
            target_name=user.get("username"),
        )
        raise


@router.delete("/{user_id}")
async def delete_user(user_id: int, current_user=Depends(require_teacher)):
    user = users_repo.get_by_id(user_id)
    if user is None:
        raise AppException(message="用户不存在", code=4042, status_code=404)

    try:
        if int(user["id"]) == int(current_user["id"]):
            raise AppException(message="不能删除当前登录账号", code=4010, status_code=400)

        if _get_student_meta(user.get("student_id")) is not None:
            raise AppException(
                message="已绑定学生档案的账号请在学生管理模块维护，不能在此删除",
                code=4011,
                status_code=400,
            )

        if (
            user.get("role") == "teacher"
            and user.get("is_active", True)
            and _count_active_teachers(exclude_user_id=user_id) == 0
        ):
            raise AppException(message="系统至少需要保留一个启用中的教师账号", code=4012, status_code=400)

        ok = users_repo.delete(user_id)
        if not ok:
            raise AppException(message="删除用户失败", code=5004, status_code=500)

        audit_log_service.record(
            operator=current_user,
            module="user_management",
            action="delete_user",
            result="success",
            message="删除用户成功",
            target_type="user",
            target_id=user_id,
            target_name=user.get("username"),
            detail={"role": user.get("role")},
        )
        return success_response(
            data={"deleted": True, "user_id": user_id},
            message="用户删除成功",
        )
    except AppException as exc:
        audit_log_service.record(
            operator=current_user,
            module="user_management",
            action="delete_user",
            result="failed",
            message=exc.message,
            target_type="user",
            target_id=user_id,
            target_name=user.get("username"),
        )
        raise
