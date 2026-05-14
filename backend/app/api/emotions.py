from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.core.deps import require_teacher
from app.services.emotion_service import emotion_service
from app.utils.response import success_response

router = APIRouter(prefix="/emotions", tags=["emotions"])


@router.get("/records")
async def list_emotion_records(
    keyword: Optional[str] = Query(default=None, description="按学号/姓名/活动名称搜索"),
    source: Optional[str] = Query(default=None, description="按来源筛选 attendance/group_photo"),
    emotion: Optional[str] = Query(default=None, description="按情绪筛选"),
    start_date: Optional[str] = Query(default=None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(default=None, description="结束日期 YYYY-MM-DD"),
    current_user=Depends(require_teacher),
):
    result = emotion_service.list_records(
        keyword=keyword,
        source=source,
        emotion=emotion,
        start_date=start_date,
        end_date=end_date,
    )
    return success_response(data=result)


@router.get("/dashboard")
async def emotion_dashboard(current_user=Depends(require_teacher)):
    return success_response(data=emotion_service.dashboard())


@router.get("/distribution")
async def emotion_distribution(current_user=Depends(require_teacher)):
    return success_response(data=emotion_service.emotion_distribution())


@router.get("/sources")
async def emotion_source_distribution(current_user=Depends(require_teacher)):
    return success_response(data=emotion_service.source_distribution())


@router.get("/students")
async def emotion_student_summary(current_user=Depends(require_teacher)):
    return success_response(data=emotion_service.student_summary())


@router.get("/trend")
async def emotion_daily_trend(current_user=Depends(require_teacher)):
    return success_response(data=emotion_service.daily_trend())


@router.get("/report")
async def emotion_report(current_user=Depends(require_teacher)):
    return success_response(data=emotion_service.report())
