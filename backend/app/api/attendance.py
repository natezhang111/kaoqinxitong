from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from fastapi.responses import FileResponse

from app.core.deps import get_current_user
from app.services.attendance_service import attendance_service
from app.services.audit_log_service import audit_log_service
from app.utils.response import success_response

router = APIRouter(prefix="/attendance", tags=["attendance"])


def _query_filters(
    keyword: Optional[str],
    class_name: Optional[str],
    status: Optional[str],
    capture_mode: Optional[str],
    liveness_result: Optional[str],
    emotion: Optional[str],
    start_date: Optional[str],
    end_date: Optional[str],
) -> dict:
    return {
        "keyword": keyword,
        "class_name": class_name,
        "status": status,
        "capture_mode": capture_mode,
        "liveness_result": liveness_result,
        "emotion": emotion,
        "start_date": start_date,
        "end_date": end_date,
    }


@router.get("")
@router.get("/records")
async def list_attendance_records(
    keyword: Optional[str] = Query(default=None, description="按姓名/学号搜索"),
    class_name: Optional[str] = Query(default=None, description="按班级筛选"),
<<<<<<< HEAD
    status: Optional[str] = Query(
        default=None, description="按状态筛选：present/unknown/rejected"
    ),
    capture_mode: Optional[str] = Query(
        default=None, description="按采集方式筛选：manual/auto"
    ),
    liveness_result: Optional[str] = Query(
        default=None, description="按活体结果筛选：real/fake"
    ),
=======
    status: Optional[str] = Query(default=None, description="按状态筛选：present/unknown/rejected"),
    capture_mode: Optional[str] = Query(default=None, description="按采集方式筛选：manual/auto"),
    liveness_result: Optional[str] = Query(default=None, description="按活体结果筛选：real/fake/uncertain"),
>>>>>>> 98bf8e49 (update)
    emotion: Optional[str] = Query(default=None, description="按情绪筛选"),
    start_date: Optional[str] = Query(default=None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(default=None, description="结束日期 YYYY-MM-DD"),
    current_user=Depends(get_current_user),
):
<<<<<<< HEAD
    filters = _query_filters(
        keyword,
        class_name,
        status,
        capture_mode,
        liveness_result,
        emotion,
        start_date,
        end_date,
    )
    records = attendance_service.list_records(current_user=current_user, **filters)
=======
    records = attendance_service.list_records(
        current_user=current_user,
        **_query_filters(
            keyword,
            class_name,
            status,
            capture_mode,
            liveness_result,
            emotion,
            start_date,
            end_date,
        ),
    )
>>>>>>> 98bf8e49 (update)
    return success_response(data=records)


@router.get("/export")
async def export_attendance_records(
    keyword: Optional[str] = Query(default=None, description="按姓名/学号搜索"),
    class_name: Optional[str] = Query(default=None, description="按班级筛选"),
    status: Optional[str] = Query(default=None, description="按状态筛选"),
    capture_mode: Optional[str] = Query(default=None, description="按采集方式筛选"),
    liveness_result: Optional[str] = Query(default=None, description="按活体结果筛选"),
    emotion: Optional[str] = Query(default=None, description="按情绪筛选"),
    start_date: Optional[str] = Query(default=None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(default=None, description="结束日期 YYYY-MM-DD"),
    current_user=Depends(get_current_user),
):
    filters = _query_filters(
        keyword,
        class_name,
        status,
        capture_mode,
        liveness_result,
        emotion,
        start_date,
        end_date,
    )
<<<<<<< HEAD
    output_path = attendance_service.export_records(
        current_user=current_user,
        **filters,
    )
=======
    output_path = attendance_service.export_records(current_user=current_user, **filters)
>>>>>>> 98bf8e49 (update)
    audit_log_service.record(
        operator=current_user,
        module="attendance",
        action="export_attendance",
        result="success",
        message="导出考勤记录成功",
        target_type="attendance",
        detail={**filters, "filename": output_path.name},
    )
    return FileResponse(
        path=output_path,
        filename=output_path.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@router.get("/{record_id}")
@router.get("/records/{record_id}")
async def get_attendance_record(record_id: int, current_user=Depends(get_current_user)):
    record = attendance_service.get_record(record_id, current_user=current_user)
    return success_response(data=record)


@router.post("/checkin")
@router.post("/recognize")
async def recognize_attendance(
<<<<<<< HEAD
    files: Optional[list[UploadFile]] = File(
        default=None, description="连续抓拍帧，建议 5 帧"
    ),
    file: Optional[UploadFile] = File(default=None, description="兼容旧版的单张图片"),
    capture_mode: str = Form(default="manual"),
    current_user=Depends(get_current_user),
):
    frame_items: list[tuple[str, bytes]] = []

=======
    files: Optional[list[UploadFile]] = File(default=None, description="连续抓拍帧，建议 9-10 帧"),
    file: Optional[UploadFile] = File(default=None, description="兼容旧版的单张图片上传"),
    capture_mode: str = Form(default="manual"),
    challenge_id: Optional[str] = Form(default=None),
    current_user=Depends(get_current_user),
):
    frame_items: list[tuple[str, bytes]] = []
>>>>>>> 98bf8e49 (update)
    if files:
        for item in files:
            frame_items.append((item.filename or "frame.png", await item.read()))
    elif file is not None:
        frame_items.append((file.filename or "frame.png", await file.read()))

    result = attendance_service.recognize_attendance(
        frame_items=frame_items,
        capture_mode=capture_mode,
        current_user=current_user,
<<<<<<< HEAD
    )

    if result["status"] == "present":
        message = "识别成功，已记录考勤"
    elif result["status"] == "rejected":
        message = "活体检测未通过，已拒绝本次考勤"
    else:
        message = "未匹配到已知学生，已记录为陌生人/未识别"
=======
        challenge_id=challenge_id,
    )

    if result["status"] == "present":
        message = result.get("reason") or "活体校验通过，已记录考勤"
    elif result["status"] == "retry":
        message = result.get("challenge_reason") or result.get("reason") or "当前样本需要重试"
    elif result["status"] == "rejected":
        message = result.get("challenge_reason") or result.get("reason") or "活体校验未通过，已拒绝本次考勤"
    else:
        message = result.get("reason") or "活体校验通过，但未匹配到已知学生"
>>>>>>> 98bf8e49 (update)

    audit_log_service.record(
        operator=current_user,
        module="attendance",
        action="checkin",
<<<<<<< HEAD
        result="success" if result["status"] == "present" else "failed",
=======
        result="success" if result["status"] in {"present", "unknown", "retry"} else "failed",
>>>>>>> 98bf8e49 (update)
        message=message,
        target_type="attendance",
        target_id=result.get("record_id"),
        target_name=result.get("student_no") or result.get("student_name"),
        detail={
            "capture_mode": capture_mode,
            "status": result.get("status"),
            "student_no": result.get("student_no"),
            "student_name": result.get("student_name"),
<<<<<<< HEAD
            "liveness_result": result.get("liveness_result"),
=======
            "challenge_id": result.get("challenge_id"),
            "challenge_result": result.get("challenge_result"),
            "challenge_score": result.get("challenge_score"),
            "challenge_threshold": result.get("challenge_threshold"),
            "challenge_action": result.get("challenge_action"),
            "challenge_action_label": result.get("challenge_action_label"),
            "challenge_prompt": result.get("challenge_prompt"),
            "challenge_reason": result.get("challenge_reason"),
            "challenge_details": result.get("challenge_details"),
            "liveness_result": result.get("liveness_result"),
            "liveness_score": result.get("liveness_score"),
            "liveness_confidence": result.get("liveness_confidence"),
            "spoof_result": result.get("spoof_result"),
            "spoof_score": result.get("spoof_score"),
            "spoof_confidence": result.get("spoof_confidence"),
            "accepted_frame_count": result.get("accepted_frame_count"),
            "rejected_frame_count": result.get("rejected_frame_count"),
            "quality_insufficient": result.get("quality_insufficient"),
            "uncertain": result.get("uncertain"),
            "reason": result.get("reason"),
>>>>>>> 98bf8e49 (update)
        },
    )
    return success_response(data=result, message=message)
