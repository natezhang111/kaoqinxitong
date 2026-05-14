from __future__ import annotations

<<<<<<< HEAD
import csv
import io
=======
>>>>>>> 98bf8e49 (update)
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Query, UploadFile
from pydantic import BaseModel, Field

from app.core.config import (
    ALLOWED_IMAGE_SUFFIXES,
    FACE_EMBEDDING_EXT,
    FACES_DIR,
    FEATURES_DIR,
)
from app.core.deps import get_current_user, require_student, require_teacher
from app.core.exceptions import AppException
from app.core.security import get_password_hash
from app.schemas.student import StudentCreate, StudentUpdate
from app.services.audit_log_service import audit_log_service
from app.services.face_engine import face_engine
<<<<<<< HEAD
=======
from app.services.student_import_service import student_import_service
>>>>>>> 98bf8e49 (update)
from app.storage.repositories import (
    activities_repo,
    activity_face_results_repo,
    attendance_repo,
    emotion_records_repo,
    students_repo,
    users_repo,
)
from app.utils.response import success_response

router = APIRouter(prefix="/students", tags=["students"])

DEFAULT_STUDENT_PASSWORD = "123456"


class StudentAccountBindRequest(BaseModel):
    username: Optional[str] = Field(default=None, min_length=1, max_length=64)
    password: str = Field(default=DEFAULT_STUDENT_PASSWORD, min_length=1, max_length=128)
    reactivate_account: bool = True


class StudentAccountResetPasswordRequest(BaseModel):
    password: str = Field(default=DEFAULT_STUDENT_PASSWORD, min_length=1, max_length=128)


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _normalize_bool(value: str | bool | None, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value

    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y", "on"}:
        return True
    if text in {"false", "0", "no", "n", "off"}:
        return False
    return default


def _validate_image_filename(filename: Optional[str]) -> str:
    if not filename:
        raise AppException(message="上传文件缺少文件名", code=4001, status_code=400)

    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_IMAGE_SUFFIXES:
        raise AppException(
            message=f"不支持的图片格式，仅支持: {sorted(ALLOWED_IMAGE_SUFFIXES)}",
            code=4002,
            status_code=400,
        )
    return suffix


def _build_feature_filename(student_no: str) -> str:
    return f"{student_no}{FACE_EMBEDDING_EXT}"


def _build_feature_relpath(student_no: str) -> str:
    return f"features/{_build_feature_filename(student_no)}"


def _build_face_relpath(filename: str) -> str:
    return f"faces/{filename}"


def _list_student_users() -> List[Dict[str, Any]]:
    return [item for item in users_repo.list_all() if item.get("role") == "student"]


def _find_student_user(student_id: int) -> Optional[Dict[str, Any]]:
    for user in _list_student_users():
        if user.get("student_id") == student_id:
            return user
    return None


def _resolve_available_student_username(preferred: str, student_id: int) -> str:
    base = preferred.strip()
    if not base:
        base = f"student_{student_id}"

    existing = users_repo.get_by_username(base)
    if existing is None or (
        existing.get("role") == "student" and existing.get("student_id") == student_id
    ):
        return base

    fallback = f"stu_{base}"
    existing = users_repo.get_by_username(fallback)
    if existing is None or (
        existing.get("role") == "student" and existing.get("student_id") == student_id
    ):
        return fallback

    final_name = f"{fallback}_{student_id}"
    existing = users_repo.get_by_username(final_name)
    if existing is None or (
        existing.get("role") == "student" and existing.get("student_id") == student_id
    ):
        return final_name

    raise AppException(message="无法为该学生分配可用账号名", code=5006, status_code=500)


def _serialize_student(student: Dict[str, Any]) -> Dict[str, Any]:
    user = _find_student_user(int(student["id"]))
    return {
        **student,
        "account_bound": user is not None,
        "account_user_id": user.get("id") if user else None,
        "account_username": user.get("username") if user else None,
        "account_is_active": user.get("is_active", True) if user else None,
    }


def _ensure_student_account(
    student: Dict[str, Any],
    *,
    username: Optional[str] = None,
    password: str = DEFAULT_STUDENT_PASSWORD,
    reactivate_account: bool = True,
    force_reset_password: bool = False,
) -> Dict[str, Any]:
    student_id = int(student["id"])
    student_user = _find_student_user(student_id)
    target_username = _resolve_available_student_username(
        username or str(student["student_no"]),
        student_id,
    )

    if student_user is None:
        existing = users_repo.get_by_username(target_username)
        if existing is not None and existing.get("student_id") not in {None, student_id}:
            raise AppException(message="目标账号名已被其他用户占用", code=4011, status_code=400)

        if existing is not None and existing.get("student_id") in {None, student_id}:
            student_user = users_repo.update(
                existing["id"],
                {
                    "role": "student",
                    "student_id": student_id,
                    "is_active": student.get("is_active", True) if reactivate_account else existing.get("is_active", True),
                    "password_hash": get_password_hash(password) if force_reset_password else existing.get("password_hash"),
                },
            )
        else:
            student_user = users_repo.create(
                {
                    "username": target_username,
                    "password_hash": get_password_hash(password),
                    "role": "student",
                    "student_id": student_id,
                    "is_active": bool(student.get("is_active", True)),
                    "created_at": _now_str(),
                }
            )
    else:
        updates = {
            "student_id": student_id,
            "is_active": bool(student.get("is_active", True))
            if reactivate_account
            else student_user.get("is_active", True),
        }
        if student_user.get("username") != target_username and username:
            duplicate = users_repo.get_by_username(target_username)
            if duplicate is not None and duplicate.get("id") != student_user.get("id"):
                raise AppException(message="目标账号名已被其他用户占用", code=4011, status_code=400)
            updates["username"] = target_username
        if force_reset_password:
            updates["password_hash"] = get_password_hash(password)
        student_user = users_repo.update(student_user["id"], updates)

    if student_user is None:
        raise AppException(message="学生账号绑定失败", code=5007, status_code=500)
    return student_user


def ensure_student_accounts_for_all_students() -> None:
    for student in students_repo.list_all():
        try:
            _ensure_student_account(student)
        except AppException:
            continue


def _get_current_student(current_user: Dict[str, Any]) -> Dict[str, Any]:
    student_id = current_user.get("student_id")
    if student_id is None:
        raise AppException(message="当前学生账号尚未绑定学生档案", code=4034, status_code=403)

    student = students_repo.get_by_id(int(student_id))
    if student is None:
        raise AppException(message="学生档案不存在", code=4041, status_code=404)
    return student


def _student_summary(student_id: int) -> Dict[str, Any]:
    attendance_records = [item for item in attendance_repo.list_all() if item.get("student_id") == student_id]
    emotion_records = [item for item in emotion_records_repo.list_all() if item.get("student_id") == student_id]
    activity_rows = [
        item
        for item in activity_face_results_repo.list_all()
        if item.get("student_id") == student_id and item.get("status") == "matched"
    ]
    unique_activity_ids = {int(item["activity_id"]) for item in activity_rows if item.get("activity_id") is not None}

    present_count = sum(1 for item in attendance_records if item.get("status") == "present")
    rejected_count = sum(1 for item in attendance_records if item.get("status") == "rejected")
    unknown_count = sum(1 for item in attendance_records if item.get("status") == "unknown")

    return {
        "attendance_count": len(attendance_records),
        "present_count": present_count,
        "rejected_count": rejected_count,
        "unknown_count": unknown_count,
        "emotion_count": len(emotion_records),
        "activity_count": len(unique_activity_ids),
    }


def _student_activities(student_id: int) -> List[Dict[str, Any]]:
    raw_rows = [
        item
        for item in activity_face_results_repo.list_all()
        if item.get("student_id") == student_id and item.get("status") == "matched"
    ]

    best_by_activity: Dict[int, Dict[str, Any]] = {}
    for row in raw_rows:
        activity_id = row.get("activity_id")
        if activity_id is None:
            continue
        activity_id = int(activity_id)
        current_best = best_by_activity.get(activity_id)
        if current_best is None or float(row.get("match_score", 0.0)) > float(
            current_best.get("match_score", 0.0)
        ):
            best_by_activity[activity_id] = row

    activities = []
    for activity_id, row in best_by_activity.items():
        activity = activities_repo.get_by_id(activity_id)
        if activity is None:
            continue
        activities.append(
            {
                "activity_id": activity_id,
                "title": activity.get("title"),
                "activity_type": activity.get("activity_type"),
                "activity_date": activity.get("activity_date"),
                "match_score": row.get("match_score"),
                "det_score": row.get("det_score"),
                "emotion": row.get("emotion"),
                "emotion_score": row.get("emotion_score"),
                "created_at": row.get("created_at"),
            }
        )

    activities.sort(
        key=lambda item: (item.get("activity_date") or "", int(item.get("activity_id", 0))),
        reverse=True,
    )
    return activities


def _student_emotions(student_id: int) -> List[Dict[str, Any]]:
    rows = [item for item in emotion_records_repo.list_all() if item.get("student_id") == student_id]
    rows.sort(key=lambda x: int(x.get("id", 0)), reverse=True)
    return rows


def _student_group_photo_records(student_id: int) -> List[Dict[str, Any]]:
    raw_rows = [
        item
        for item in activity_face_results_repo.list_all()
        if item.get("student_id") == student_id
        and item.get("status") == "matched"
        and item.get("activity_id") is not None
    ]

    grouped: Dict[int, Dict[str, Any]] = {}
    for row in raw_rows:
        activity_id = int(row["activity_id"])
        activity = activities_repo.get_by_id(activity_id)
        if activity is None:
            continue

        current = grouped.get(activity_id)
        match_score = float(row.get("match_score", 0.0) or 0.0)
        det_score = float(row.get("det_score", 0.0) or 0.0)

        if current is None:
            current = {
                "activity_id": activity_id,
                "title": activity.get("title"),
                "activity_type": activity.get("activity_type"),
                "activity_date": activity.get("activity_date"),
                "image_path": activity.get("image_path"),
                "face_count": activity.get("face_count", 0),
                "matched_count": activity.get("matched_count", 0),
                "participant_count": activity.get("participant_count", 0),
                "recognized_face_count": 0,
                "best_match_score": 0.0,
                "average_match_score": 0.0,
                "best_det_score": 0.0,
                "latest_emotion": row.get("emotion"),
                "latest_emotion_score": row.get("emotion_score"),
                "first_recognized_at": row.get("created_at"),
                "latest_recognized_at": row.get("created_at"),
            }
            grouped[activity_id] = current

        current["recognized_face_count"] += 1
        current["average_match_score"] += match_score
        current["best_match_score"] = max(float(current["best_match_score"]), match_score)
        current["best_det_score"] = max(float(current["best_det_score"]), det_score)

        created_at = row.get("created_at")
        if created_at and (
            not current.get("first_recognized_at")
            or str(created_at) < str(current["first_recognized_at"])
        ):
            current["first_recognized_at"] = created_at
        if created_at and (
            not current.get("latest_recognized_at")
            or str(created_at) > str(current["latest_recognized_at"])
        ):
            current["latest_recognized_at"] = created_at
            current["latest_emotion"] = row.get("emotion")
            current["latest_emotion_score"] = row.get("emotion_score")

    records = []
    for item in grouped.values():
        count = int(item.get("recognized_face_count", 0) or 0)
        item["average_match_score"] = round(
            float(item.get("average_match_score", 0.0)) / count if count else 0.0,
            6,
        )
        item["best_match_score"] = round(float(item.get("best_match_score", 0.0)), 6)
        item["best_det_score"] = round(float(item.get("best_det_score", 0.0)), 6)
        records.append(item)

    records.sort(
        key=lambda item: (
            item.get("activity_date") or "",
            item.get("latest_recognized_at") or "",
            int(item.get("activity_id", 0)),
        ),
        reverse=True,
    )
    return records


@router.get("")
async def list_students(
    keyword: Optional[str] = Query(default=None, description="按姓名或学号模糊搜索"),
    class_name: Optional[str] = Query(default=None, description="按班级筛选"),
    is_active: Optional[bool] = Query(default=None, description="按启用状态筛选"),
    current_user=Depends(require_teacher),
):
    students = students_repo.query_students(
        keyword=keyword,
        class_name=class_name,
        is_active=is_active,
    )
    return success_response(data=[_serialize_student(item) for item in students])


@router.get("/me/profile")
async def get_my_student_profile(current_user=Depends(require_student)):
    student = _get_current_student(current_user)
    payload = _serialize_student(student)
    payload["summary"] = _student_summary(int(student["id"]))
    return success_response(data=payload)


@router.get("/me/activities")
async def list_my_student_activities(current_user=Depends(require_student)):
    student = _get_current_student(current_user)
    return success_response(data=_student_activities(int(student["id"])))


@router.get("/me/emotions")
async def list_my_student_emotions(current_user=Depends(require_student)):
    student = _get_current_student(current_user)
    return success_response(data=_student_emotions(int(student["id"])))


@router.get("/me/group-photo-records")
async def list_my_group_photo_records(current_user=Depends(require_student)):
    student = _get_current_student(current_user)
    return success_response(data=_student_group_photo_records(int(student["id"])))


@router.get("/{student_id}")
async def get_student(student_id: int, current_user=Depends(require_teacher)):
    student = students_repo.get_by_id(student_id)
    if student is None:
        raise AppException(message="学生不存在", code=4041, status_code=404)
    return success_response(data=_serialize_student(student))


@router.get("/{student_id}/account")
async def get_student_account(student_id: int, current_user=Depends(require_teacher)):
    student = students_repo.get_by_id(student_id)
    if student is None:
        raise AppException(message="学生不存在", code=4041, status_code=404)

    user = _find_student_user(student_id)
    return success_response(
        data={
            "student_id": student_id,
            "student_no": student.get("student_no"),
            "account_bound": user is not None,
            "account_user_id": user.get("id") if user else None,
            "username": user.get("username") if user else None,
            "is_active": user.get("is_active", True) if user else None,
            "default_password": DEFAULT_STUDENT_PASSWORD,
        }
    )


@router.post("")
async def create_student(payload: StudentCreate, current_user=Depends(require_teacher)):
    existing = students_repo.get_by_student_no(payload.student_no)
    if existing is not None:
        raise AppException(message="学号已存在", code=4004, status_code=400)

    student = students_repo.create(
        {
            "student_no": payload.student_no,
            "name": payload.name,
            "class_name": payload.class_name,
            "is_active": payload.is_active,
            "face_image_path": None,
            "face_feature_path": _build_feature_relpath(payload.student_no),
            "feature_status": "pending",
            "created_at": _now_str(),
        }
    )
    account = _ensure_student_account(student)
    audit_log_service.record(
        operator=current_user,
        module="student_management",
        action="create_student",
        result="success",
        message="创建学生成功",
        target_type="student",
        target_id=int(student["id"]),
        target_name=student.get("student_no"),
        detail={
            "student_no": student.get("student_no"),
            "name": student.get("name"),
            "class_name": student.get("class_name"),
            "account_username": account.get("username"),
        },
    )
    return success_response(
        data={
            **_serialize_student(student),
            "default_password": DEFAULT_STUDENT_PASSWORD,
            "created_account_username": account["username"],
        },
        message="学生创建成功，已自动生成学生账号",
    )


@router.post("/{student_id}/account/bind")
async def bind_student_account(
    student_id: int,
    payload: StudentAccountBindRequest,
    current_user=Depends(require_teacher),
):
    student = students_repo.get_by_id(student_id)
    if student is None:
        raise AppException(message="学生不存在", code=4041, status_code=404)

    account = _ensure_student_account(
        student,
        username=payload.username,
        password=payload.password,
        reactivate_account=payload.reactivate_account,
        force_reset_password=True,
    )
    audit_log_service.record(
        operator=current_user,
        module="student_management",
        action="bind_student_account",
        result="success",
        message="绑定学生账号成功",
        target_type="student",
        target_id=student_id,
        target_name=student.get("student_no"),
        detail={"account_username": account.get("username")},
    )
    return success_response(
        data={
            "student_id": student_id,
            "student_no": student.get("student_no"),
            "account_user_id": account["id"],
            "username": account["username"],
            "is_active": account.get("is_active", True),
            "default_password": payload.password,
        },
        message="学生账号绑定成功",
    )


@router.post("/{student_id}/account/reset-password")
async def reset_student_account_password(
    student_id: int,
    payload: StudentAccountResetPasswordRequest,
    current_user=Depends(require_teacher),
):
    student = students_repo.get_by_id(student_id)
    if student is None:
        raise AppException(message="学生不存在", code=4041, status_code=404)

    account = _find_student_user(student_id)
    if account is None:
        account = _ensure_student_account(
            student,
            password=payload.password,
            force_reset_password=True,
        )
    else:
        account = users_repo.update(
            account["id"],
            {
                "password_hash": get_password_hash(payload.password),
                "is_active": bool(student.get("is_active", True)),
            },
        )

    audit_log_service.record(
        operator=current_user,
        module="student_management",
        action="reset_student_password",
        result="success",
        message="重置学生账号密码成功",
        target_type="student",
        target_id=student_id,
        target_name=student.get("student_no"),
        detail={"account_username": account["username"] if account else None},
    )
    return success_response(
        data={
            "student_id": student_id,
            "student_no": student.get("student_no"),
            "account_user_id": account["id"] if account else None,
            "username": account["username"] if account else None,
            "reset_password": payload.password,
        },
        message="学生账号密码已重置",
    )


@router.put("/{student_id}")
async def update_student(
    student_id: int,
    payload: StudentUpdate,
    current_user=Depends(require_teacher),
):
    student = students_repo.get_by_id(student_id)
    if student is None:
        raise AppException(message="学生不存在", code=4041, status_code=404)

    updates = payload.model_dump(exclude_unset=True)
    updated = students_repo.update(student_id, updates)
    if updated is None:
        raise AppException(message="学生更新失败", code=5001, status_code=500)

    linked_user = _find_student_user(student_id)
    if linked_user is not None and "is_active" in updates:
        users_repo.update(
            linked_user["id"],
            {
                "is_active": bool(updated.get("is_active", True)),
            },
        )

    audit_log_service.record(
        operator=current_user,
        module="student_management",
        action="update_student",
        result="success",
        message="更新学生信息成功",
        target_type="student",
        target_id=student_id,
        target_name=updated.get("student_no"),
        detail={"updates": updates},
    )
    return success_response(data=_serialize_student(updated), message="学生更新成功")


@router.delete("/{student_id}")
async def delete_student(student_id: int, current_user=Depends(require_teacher)):
    student = students_repo.get_by_id(student_id)
    if student is None:
        raise AppException(message="学生不存在", code=4041, status_code=404)

    linked_users = [item for item in _list_student_users() if item.get("student_id") == student_id]
    for user in linked_users:
        users_repo.delete(int(user["id"]))

    ok = students_repo.delete(student_id)
    if not ok:
        raise AppException(message="删除失败", code=5002, status_code=500)

    audit_log_service.record(
        operator=current_user,
        module="student_management",
        action="delete_student",
        result="success",
        message="删除学生成功",
        target_type="student",
        target_id=student_id,
        target_name=student.get("student_no"),
        detail={"deleted_account_count": len(linked_users)},
    )
    return success_response(
        data={
            "deleted": True,
            "student_id": student_id,
            "deleted_account_count": len(linked_users),
        },
        message="学生删除成功",
    )


@router.post("/import")
async def import_students_csv(
    file: UploadFile = File(
        ..., description="CSV 文件，表头至少包含 student_no,name,class_name"
    ),
<<<<<<< HEAD
    current_user=Depends(require_teacher),
):
    filename = file.filename or ""
    if not filename.lower().endswith(".csv"):
        raise AppException(message="仅支持上传 CSV 文件", code=4005, status_code=400)

    content_bytes = await file.read()
    if not content_bytes:
        raise AppException(message="CSV 文件内容为空", code=4006, status_code=400)

    try:
        text = content_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise AppException(message="CSV 文件编码需为 UTF-8", code=4007, status_code=400)

    reader = csv.DictReader(io.StringIO(text))
    required_columns = {"student_no", "name", "class_name"}
    if reader.fieldnames is None:
        raise AppException(message="CSV 缺少表头", code=4008, status_code=400)

    fieldnames = {name.strip() for name in reader.fieldnames if name}
    if not required_columns.issubset(fieldnames):
        raise AppException(
            message="CSV 表头必须包含: student_no,name,class_name",
            code=4009,
            status_code=400,
        )

    created = []
    skipped = []

    for idx, row in enumerate(reader, start=2):
        student_no = str(row.get("student_no", "")).strip()
        name = str(row.get("name", "")).strip()
        class_name = str(row.get("class_name", "")).strip()
        is_active = _normalize_bool(row.get("is_active"), default=True)

        if not student_no or not name or not class_name:
            skipped.append(
                {
                    "row": idx,
                    "reason": "student_no、name、class_name 不能为空",
                }
            )
            continue

        existing = students_repo.get_by_student_no(student_no)
        if existing is not None:
            skipped.append(
                {
                    "row": idx,
                    "student_no": student_no,
                    "reason": "学号已存在，已跳过",
                }
            )
            continue

        student = students_repo.create(
            {
                "student_no": student_no,
                "name": name,
                "class_name": class_name,
                "is_active": is_active,
                "face_image_path": None,
                "face_feature_path": _build_feature_relpath(student_no),
                "feature_status": "pending",
                "created_at": _now_str(),
            }
        )
        _ensure_student_account(student)
        created.append(_serialize_student(student))
=======
    photos_zip: Optional[UploadFile] = File(
        default=None, description="可选：学生照片 ZIP，照片文件名建议使用学号命名"
    ),
    current_user=Depends(require_teacher),
):
    filename = file.filename or ""
    content_bytes = await file.read()
    photos_zip_bytes = await photos_zip.read() if photos_zip is not None else None

    result = student_import_service.import_students(
        csv_bytes=content_bytes,
        csv_filename=filename,
        photos_zip_bytes=photos_zip_bytes,
        photos_zip_filename=photos_zip.filename if photos_zip is not None else None,
        ensure_student_account=_ensure_student_account,
        serialize_student=_serialize_student,
    )
>>>>>>> 98bf8e49 (update)

    audit_log_service.record(
        operator=current_user,
        module="student_management",
        action="import_students",
        result="success",
        message="批量导入学生完成",
        target_type="student",
        detail={
<<<<<<< HEAD
            "created_count": len(created),
            "skipped_count": len(skipped),
            "filename": filename,
        },
    )
    return success_response(
        data={
            "created_count": len(created),
            "skipped_count": len(skipped),
            "default_password": DEFAULT_STUDENT_PASSWORD,
            "created": created,
            "skipped": skipped,
        },
        message="批量导入完成，已自动生成学生账号",
=======
            "created_count": result["created_count"],
            "skipped_count": result["skipped_count"],
            "photo_bound_count": result["photo_bound_count"],
            "photo_missing_count": result["photo_missing_count"],
            "photo_failed_count": result["photo_failed_count"],
            "unmatched_photo_count": result["unmatched_photo_count"],
            "duplicate_photo_count": result["duplicate_photo_count"],
            "filename": filename,
            "photos_zip_filename": photos_zip.filename if photos_zip is not None else None,
        },
    )
    return success_response(
        data=result,
        message=(
            "批量导入完成，已自动生成学生账号"
            if photos_zip is None
            else "批量导入完成，已同时处理学生照片与人脸特征"
        ),
>>>>>>> 98bf8e49 (update)
    )


@router.post("/{student_id}/face")
async def upload_student_face(
    student_id: int,
    file: UploadFile = File(..., description="学生人脸照片"),
    current_user=Depends(require_teacher),
):
    student = students_repo.get_by_id(student_id)
    if student is None:
        raise AppException(message="学生不存在", code=4041, status_code=404)

    suffix = _validate_image_filename(file.filename)

    file_bytes = await file.read()
    if not file_bytes:
        raise AppException(message="上传的图片为空", code=4010, status_code=400)

    student_no = str(student["student_no"])
    unique_name = f"{student_no}_{uuid4().hex}{suffix}"
    image_save_path = FACES_DIR / unique_name

    feature_filename = _build_feature_filename(student_no)
    feature_save_path = FEATURES_DIR / feature_filename

    image_save_path.write_bytes(file_bytes)

    try:
        result = face_engine.extract_single_face_embedding(image_save_path)
        embedding = result["embedding"]
        face_engine.save_embedding(embedding, feature_save_path)
    except Exception:
        if image_save_path.exists():
            image_save_path.unlink(missing_ok=True)
        raise

    face_relpath = _build_face_relpath(unique_name)
    feature_relpath = _build_feature_relpath(student_no)

    updated = students_repo.update(
        student_id,
        {
            "face_image_path": face_relpath,
            "face_feature_path": feature_relpath,
            "feature_status": "ready",
        },
    )
    if updated is None:
        raise AppException(message="保存学生照片信息失败", code=5003, status_code=500)

    audit_log_service.record(
        operator=current_user,
        module="student_management",
        action="upload_student_face",
        result="success",
        message="上传学生注册照成功",
        target_type="student",
        target_id=student_id,
        target_name=student_no,
        detail={"feature_status": "ready"},
    )
    return success_response(
        data={
            "student_id": student_id,
            "student_no": student_no,
            "face_image_path": face_relpath,
            "face_feature_path": feature_relpath,
            "feature_status": "ready",
            "embedding_dim": result["embedding_dim"],
            "det_score": result["det_score"],
            "bbox": result["bbox"],
        },
        message="学生照片上传成功，已完成人脸检测与特征提取",
    )
