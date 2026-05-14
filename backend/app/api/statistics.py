from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.core.deps import require_teacher
from app.services.audit_log_service import audit_log_service
from app.services.statistics_service import statistics_service
from app.utils.response import success_response

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/dashboard")
async def statistics_dashboard(current_user=Depends(require_teacher)):
    return success_response(data=statistics_service.dashboard())


@router.get("/activity-frequency")
async def statistics_activity_frequency(current_user=Depends(require_teacher)):
    return success_response(data=statistics_service.activity_frequency())


@router.get("/activity-accuracy")
async def statistics_activity_accuracy(current_user=Depends(require_teacher)):
    return success_response(data=statistics_service.activity_accuracy())


@router.get("/activity-type-distribution")
async def statistics_activity_type_distribution(current_user=Depends(require_teacher)):
    return success_response(data=statistics_service.activity_type_distribution())


@router.get("/report")
async def statistics_report(current_user=Depends(require_teacher)):
    return success_response(data=statistics_service.report())


@router.get("/report/export")
async def export_statistics_report_excel(current_user=Depends(require_teacher)):
    output_path = statistics_service.export_report()
    audit_log_service.record(
        operator=current_user,
        module="statistics",
        action="export_statistics_report",
        result="success",
        message="导出统计报表成功",
        target_type="report",
        target_name=output_path.name,
    )
    return FileResponse(
        path=output_path,
        filename=output_path.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
