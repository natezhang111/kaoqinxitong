from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
<<<<<<< HEAD
=======
from fastapi.responses import FileResponse
>>>>>>> 98bf8e49 (update)

from app.core.deps import require_teacher
from app.services.audit_log_service import audit_log_service
from app.utils.response import success_response

router = APIRouter(prefix="/audit-logs", tags=["audit-logs"])


@router.get("/records")
async def list_audit_logs(
<<<<<<< HEAD
    keyword: Optional[str] = Query(default=None, description="按操作人、模块、动作或消息搜索"),
    module: Optional[str] = Query(default=None, description="按模块筛选"),
    action: Optional[str] = Query(default=None, description="按动作筛选"),
    result: Optional[str] = Query(default=None, description="按结果筛选：success/failed"),
    operator_username: Optional[str] = Query(default=None, description="按操作用户名筛选"),
    operator_role: Optional[str] = Query(default=None, description="按操作角色筛选"),
=======
    keyword: Optional[str] = Query(
        default=None, description="按操作人、模块、动作或消息搜索"
    ),
    module: Optional[str] = Query(default=None, description="按模块筛选"),
    action: Optional[str] = Query(default=None, description="按动作筛选"),
    result: Optional[str] = Query(
        default=None, description="按结果筛选：success/failed"
    ),
    operator_username: Optional[str] = Query(
        default=None, description="按操作用户名筛选"
    ),
    operator_role: Optional[str] = Query(default=None, description="按操作角色筛选"),
    target_name: Optional[str] = Query(default=None, description="按目标对象筛选"),
>>>>>>> 98bf8e49 (update)
    start_date: Optional[str] = Query(default=None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(default=None, description="结束日期 YYYY-MM-DD"),
    current_user=Depends(require_teacher),
):
    records = audit_log_service.list_records(
        keyword=keyword,
        module=module,
        action=action,
        result=result,
        operator_username=operator_username,
        operator_role=operator_role,
<<<<<<< HEAD
=======
        target_name=target_name,
>>>>>>> 98bf8e49 (update)
        start_date=start_date,
        end_date=end_date,
    )
    return success_response(data=records)


@router.get("/summary")
async def audit_log_summary(
    keyword: Optional[str] = Query(default=None),
    module: Optional[str] = Query(default=None),
    action: Optional[str] = Query(default=None),
    result: Optional[str] = Query(default=None),
    operator_username: Optional[str] = Query(default=None),
    operator_role: Optional[str] = Query(default=None),
<<<<<<< HEAD
=======
    target_name: Optional[str] = Query(default=None),
>>>>>>> 98bf8e49 (update)
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
    current_user=Depends(require_teacher),
):
    records = audit_log_service.list_records(
        keyword=keyword,
        module=module,
        action=action,
        result=result,
        operator_username=operator_username,
        operator_role=operator_role,
<<<<<<< HEAD
=======
        target_name=target_name,
>>>>>>> 98bf8e49 (update)
        start_date=start_date,
        end_date=end_date,
    )
    return success_response(data=audit_log_service.summary(records))
<<<<<<< HEAD
=======


@router.get("/records/export")
async def export_audit_logs(
    keyword: Optional[str] = Query(default=None),
    module: Optional[str] = Query(default=None),
    action: Optional[str] = Query(default=None),
    result: Optional[str] = Query(default=None),
    operator_username: Optional[str] = Query(default=None),
    operator_role: Optional[str] = Query(default=None),
    target_name: Optional[str] = Query(default=None),
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
    current_user=Depends(require_teacher),
):
    output_path = audit_log_service.export_records(
        keyword=keyword,
        module=module,
        action=action,
        result=result,
        operator_username=operator_username,
        operator_role=operator_role,
        target_name=target_name,
        start_date=start_date,
        end_date=end_date,
    )
    audit_log_service.record(
        operator=current_user,
        module="audit_log",
        action="export_audit_logs",
        result="success",
        message="导出操作日志成功",
        target_type="report",
        target_name=output_path.name,
        detail={
            "keyword": keyword,
            "module": module,
            "action": action,
            "result": result,
            "operator_username": operator_username,
            "operator_role": operator_role,
            "target_name": target_name,
            "start_date": start_date,
            "end_date": end_date,
        },
    )
    return FileResponse(
        path=output_path,
        filename=output_path.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
>>>>>>> 98bf8e49 (update)
