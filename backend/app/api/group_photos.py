from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.core.deps import require_teacher
from app.services.audit_log_service import audit_log_service
from app.services.evaluation_service import evaluation_service
from app.services.group_photo_service import group_photo_service
from app.utils.response import success_response

router = APIRouter(prefix="/group-photos", tags=["group-photos"])


class ActivityEvaluateRequest(BaseModel):
    actual_student_count: int = Field(..., ge=1)
    correct_match_count: int = Field(..., ge=0)
    remark: Optional[str] = None


class FaceCorrectionRequest(BaseModel):
    action: str = Field(..., min_length=1, max_length=32)
    student_id: Optional[int] = None
    note: Optional[str] = Field(default=None, max_length=500)


@router.post("/recognize")
async def recognize_group_photo(
    file: UploadFile = File(..., description="活动合照"),
    title: str = Form(..., description="活动名称"),
    activity_type: str = Form(default="class_activity", description="活动类型"),
    activity_date: Optional[str] = Form(default=None, description="活动日期 YYYY-MM-DD"),
    current_user=Depends(require_teacher),
):
    file_bytes = await file.read()
    result = group_photo_service.recognize_group_photo(
        file_bytes=file_bytes,
        filename=file.filename,
        title=title,
        activity_type=activity_type,
        activity_date=activity_date,
        current_user=current_user,
    )
    audit_log_service.record(
        operator=current_user,
        module="group_photo",
        action="recognize_group_photo",
        result="success",
        message="合照识别完成",
        target_type="activity",
        target_id=result.get("activity_id"),
        target_name=result.get("title"),
        detail={
            "face_count": result.get("face_count"),
            "matched_count": result.get("matched_count"),
            "participant_count": result.get("participant_count"),
        },
    )
    return success_response(data=result, message="合照识别完成")


@router.get("/activities")
async def list_group_photo_activities(
    keyword: Optional[str] = Query(default=None, description="按活动名称搜索"),
    activity_type: Optional[str] = Query(default=None, description="按活动类型筛选"),
    activity_date: Optional[str] = Query(default=None, description="按活动日期筛选"),
    current_user=Depends(require_teacher),
):
    result = group_photo_service.list_activities(
        keyword=keyword,
        activity_type=activity_type,
        activity_date=activity_date,
    )
    return success_response(data=result)


@router.get("/activities/{activity_id}")
async def get_group_photo_activity(
    activity_id: int,
    current_user=Depends(require_teacher),
):
    result = group_photo_service.get_activity(activity_id)
    return success_response(data=result)


@router.get("/activities/{activity_id}/participants")
async def list_group_photo_participants(
    activity_id: int,
    include_unknown: bool = Query(default=False, description="是否包含未匹配人脸"),
    current_user=Depends(require_teacher),
):
    result = group_photo_service.list_activity_participants(
        activity_id=activity_id,
        include_unknown=include_unknown,
    )
    return success_response(data=result)


@router.get("/activities/{activity_id}/export")
async def export_group_photo_activity(
    activity_id: int,
    current_user=Depends(require_teacher),
):
    output_path = group_photo_service.export_activity(activity_id)
    audit_log_service.record(
        operator=current_user,
        module="group_photo",
        action="export_activity",
        result="success",
        message="导出合照活动结果成功",
        target_type="activity",
        target_id=activity_id,
        target_name=output_path.name,
    )
    return FileResponse(
        path=output_path,
        filename=output_path.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@router.patch("/activities/{activity_id}/faces/{face_result_id}")
async def correct_group_photo_face_result(
    activity_id: int,
    face_result_id: int,
    payload: FaceCorrectionRequest,
    current_user=Depends(require_teacher),
):
    result = group_photo_service.correct_face_result(
        activity_id=activity_id,
        face_result_id=face_result_id,
        action=payload.action,
        student_id=payload.student_id,
        note=payload.note,
        operator=current_user,
    )
    audit_log_service.record(
        operator=current_user,
        module="group_photo",
        action="correct_face_result",
        result="success",
        message="合照识别结果人工修正成功",
        target_type="activity_face_result",
        target_id=face_result_id,
        target_name=str(activity_id),
        detail={
            "activity_id": activity_id,
            "action": payload.action,
            "student_id": payload.student_id,
        },
    )
    return success_response(data=result, message="合照识别结果已修正")


@router.post("/activities/{activity_id}/evaluate")
async def evaluate_group_photo_activity(
    activity_id: int,
    payload: ActivityEvaluateRequest,
    current_user=Depends(require_teacher),
):
    result = evaluation_service.evaluate_activity(
        activity_id=activity_id,
        actual_student_count=payload.actual_student_count,
        correct_match_count=payload.correct_match_count,
        remark=payload.remark,
        operator=current_user,
    )
    audit_log_service.record(
        operator=current_user,
        module="group_photo",
        action="evaluate_activity",
        result="success",
        message="活动识别准确率评估已保存",
        target_type="activity",
        target_id=activity_id,
        detail={
            "actual_student_count": payload.actual_student_count,
            "correct_match_count": payload.correct_match_count,
            "accuracy": result.get("accuracy"),
        },
    )
    return success_response(data=result, message="活动准确率评估已保存")
