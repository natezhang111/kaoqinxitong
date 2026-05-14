from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from app.core.config import DATETIME_FORMAT
from app.core.exceptions import AppException
from app.storage.repositories import activities_repo, evaluation_records_repo


class EvaluationService:
    @staticmethod
    def now_str() -> str:
        return datetime.now().strftime(DATETIME_FORMAT)

    def evaluate_activity(
        self,
        *,
        activity_id: int,
        actual_student_count: int,
        correct_match_count: int,
        remark: Optional[str] = None,
        operator: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        activity = activities_repo.get_by_id(activity_id)
        if activity is None:
            raise AppException(message="活动记录不存在", code=4042, status_code=404)

        if actual_student_count <= 0:
            raise AppException(
                message="实际参与人数必须大于 0",
                code=4229,
                status_code=422,
            )
        if correct_match_count < 0:
            raise AppException(
                message="正确识别人数不能为负数",
                code=4230,
                status_code=422,
            )
        if correct_match_count > actual_student_count:
            raise AppException(
                message="正确识别人数不能大于实际参与人数",
                code=4231,
                status_code=422,
            )

        accuracy = round(correct_match_count / actual_student_count, 6)
        created_at = self.now_str()

        existing = None
        for item in evaluation_records_repo.list_all():
            if item.get("activity_id") == activity_id:
                existing = item
                break

        payload = {
            "activity_id": activity_id,
            "actual_student_count": actual_student_count,
            "correct_match_count": correct_match_count,
            "accuracy": accuracy,
            "created_at": created_at,
            "remark": remark,
            "operator_username": operator.get("username") if operator else None,
        }

        if existing is None:
            record = evaluation_records_repo.create(payload)
        else:
            record = evaluation_records_repo.update(existing["id"], payload)

        activities_repo.update(
            activity_id,
            {
                "evaluation_accuracy": accuracy,
                "evaluation_actual_student_count": actual_student_count,
                "evaluation_correct_match_count": correct_match_count,
                "evaluation_updated_at": created_at,
            },
        )

        return {
            "activity_id": activity_id,
            "title": activity.get("title"),
            "actual_student_count": actual_student_count,
            "correct_match_count": correct_match_count,
            "accuracy": accuracy,
            "remark": remark,
            "created_at": created_at,
            "evaluation_id": record["id"] if record else None,
        }


evaluation_service = EvaluationService()
