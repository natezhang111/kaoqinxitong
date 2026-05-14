from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from fastapi.responses import FileResponse

from app.core.deps import require_teacher
from app.services.audit_log_service import audit_log_service
from app.services.security_test_service import security_test_service
from app.utils.response import success_response

router = APIRouter(prefix="/security-tests", tags=["security-tests"])


def _build_query(
    keyword: Optional[str],
    test_type: Optional[str],
    result: Optional[str],
    liveness_mode: Optional[str],
    operator_username: Optional[str],
    start_date: Optional[str],
    end_date: Optional[str],
) -> dict:
    return {
        "keyword": keyword,
        "test_type": test_type,
        "result": result,
        "liveness_mode": liveness_mode,
        "operator_username": operator_username,
        "start_date": start_date,
        "end_date": end_date,
    }


@router.get("/records")
async def list_security_test_records(
<<<<<<< HEAD
    keyword: Optional[str] = Query(default=None, description="按备注、模式、操作人搜索"),
    test_type: Optional[str] = Query(default=None, description="按测试类型筛选"),
    result: Optional[str] = Query(default=None, description="按结果筛选 real/fake"),
=======
    keyword: Optional[str] = Query(default=None, description="按备注/操作人/模型搜索"),
    test_type: Optional[str] = Query(default=None, description="按测试类型筛选"),
    result: Optional[str] = Query(default=None, description="按结果筛选：real/fake/uncertain"),
>>>>>>> 98bf8e49 (update)
    liveness_mode: Optional[str] = Query(default=None, description="按活体模式筛选"),
    operator_username: Optional[str] = Query(default=None, description="按操作人筛选"),
    start_date: Optional[str] = Query(default=None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(default=None, description="结束日期 YYYY-MM-DD"),
    current_user=Depends(require_teacher),
):
<<<<<<< HEAD
    query = _build_query(
        keyword,
        test_type,
        result,
        liveness_mode,
        operator_username,
        start_date,
        end_date,
    )
    records = security_test_service.list_records(**query)
=======
    records = security_test_service.list_records(
        **_build_query(
            keyword,
            test_type,
            result,
            liveness_mode,
            operator_username,
            start_date,
            end_date,
        )
    )
>>>>>>> 98bf8e49 (update)
    return success_response(data=records)


@router.get("/summary")
async def security_test_summary(
    keyword: Optional[str] = Query(default=None),
    test_type: Optional[str] = Query(default=None),
    result: Optional[str] = Query(default=None),
    liveness_mode: Optional[str] = Query(default=None),
    operator_username: Optional[str] = Query(default=None),
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
    current_user=Depends(require_teacher),
):
<<<<<<< HEAD
    query = _build_query(
        keyword,
        test_type,
        result,
        liveness_mode,
        operator_username,
        start_date,
        end_date,
    )
    return success_response(data=security_test_service.summary(**query))
=======
    return success_response(
        data=security_test_service.summary(
            **_build_query(
                keyword,
                test_type,
                result,
                liveness_mode,
                operator_username,
                start_date,
                end_date,
            )
        )
    )
>>>>>>> 98bf8e49 (update)


@router.get("/export")
async def export_security_test_records(
    keyword: Optional[str] = Query(default=None),
    test_type: Optional[str] = Query(default=None),
    result: Optional[str] = Query(default=None),
    liveness_mode: Optional[str] = Query(default=None),
    operator_username: Optional[str] = Query(default=None),
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
    current_user=Depends(require_teacher),
):
    query = _build_query(
        keyword,
        test_type,
        result,
        liveness_mode,
        operator_username,
        start_date,
        end_date,
    )
    output_path = security_test_service.export_records(**query)
    audit_log_service.record(
        operator=current_user,
        module="security_test",
        action="export_security_tests",
        result="success",
        message="导出安全测试记录成功",
        target_type="report",
        target_name=output_path.name,
        detail=query,
    )
    return FileResponse(
        path=output_path,
        filename=output_path.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@router.post("/liveness")
async def run_liveness_security_test(
<<<<<<< HEAD
    files: Optional[list[UploadFile]] = File(default=None, description="测试帧序列"),
    file: Optional[UploadFile] = File(default=None, description="兼容单帧上传"),
    test_type: str = Form(default="live_sample"),
    remark: Optional[str] = Form(default=None),
=======
    files: Optional[list[UploadFile]] = File(default=None, description="实时采集帧"),
    file: Optional[UploadFile] = File(default=None, description="兼容单帧上传"),
    test_type: str = Form(default="real_person"),
    remark: Optional[str] = Form(default=None),
    challenge_id: Optional[str] = Form(default=None),
>>>>>>> 98bf8e49 (update)
    current_user=Depends(require_teacher),
):
    frame_items: list[tuple[str, bytes]] = []
    if files:
        for item in files:
            frame_items.append((item.filename or "frame.png", await item.read()))
    elif file is not None:
        frame_items.append((file.filename or "frame.png", await file.read()))

    result = security_test_service.run_liveness_test(
        frame_items=frame_items,
        test_type=test_type,
        remark=remark,
        operator=current_user,
<<<<<<< HEAD
=======
        challenge_id=challenge_id,
>>>>>>> 98bf8e49 (update)
    )
    audit_log_service.record(
        operator=current_user,
        module="security_test",
        action="run_liveness_test",
<<<<<<< HEAD
        result="success",
        message="安全测试完成",
=======
        result="success" if result.get("record_id") else ("success" if result.get("uncertain") else "failed"),
        message=result.get("reason") or "安全测试完成",
>>>>>>> 98bf8e49 (update)
        target_type="security_test",
        target_id=result.get("record_id"),
        target_name=test_type,
        detail={
            "test_type": test_type,
<<<<<<< HEAD
            "frame_count": result.get("frame_count"),
            "valid_frame_count": result.get("valid_frame_count"),
            "result": result.get("result"),
            "score": result.get("score"),
        },
    )
    return success_response(data=result, message="安全测试完成")
=======
            "challenge_id": result.get("challenge_id"),
            "challenge_result": result.get("challenge_result"),
            "challenge_score": result.get("challenge_score"),
            "challenge_threshold": result.get("challenge_threshold"),
            "challenge_action": result.get("challenge_action"),
            "challenge_action_label": result.get("challenge_action_label"),
            "challenge_prompt": result.get("challenge_prompt"),
            "challenge_reason": result.get("challenge_reason"),
            "frame_count": result.get("frame_count"),
            "valid_frame_count": result.get("valid_frame_count"),
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
        },
    )
    return success_response(data=result, message=result.get("reason") or "安全测试完成")
>>>>>>> 98bf8e49 (update)
