from __future__ import annotations

from collections import Counter
from datetime import datetime
<<<<<<< HEAD
from typing import Any, Dict, Iterable, Optional

from app.core.config import DATETIME_FORMAT
=======
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from app.core.config import DATETIME_FORMAT, REPORTS_DIR
from app.storage.excel_exporter import export_audit_log_records
>>>>>>> 98bf8e49 (update)
from app.storage.repositories import audit_logs_repo


class AuditLogService:
    @staticmethod
    def now_str() -> str:
        return datetime.now().strftime(DATETIME_FORMAT)

    def _sanitize_detail(self, value: Any) -> Any:
        if value is None or isinstance(value, (bool, int, float, str)):
            return value
        if isinstance(value, datetime):
            return value.strftime(DATETIME_FORMAT)
        if isinstance(value, dict):
<<<<<<< HEAD
            return {str(key): self._sanitize_detail(item) for key, item in value.items()}
=======
            return {
                str(key): self._sanitize_detail(item) for key, item in value.items()
            }
>>>>>>> 98bf8e49 (update)
        if isinstance(value, (list, tuple, set)):
            return [self._sanitize_detail(item) for item in value]
        return str(value)

    def record(
        self,
        *,
        module: str,
        action: str,
        result: str = "success",
        message: Optional[str] = None,
        operator: Optional[Dict[str, Any]] = None,
        operator_user_id: Optional[int] = None,
        operator_username: Optional[str] = None,
        operator_role: Optional[str] = None,
        target_type: Optional[str] = None,
        target_id: Optional[int] = None,
        target_name: Optional[str] = None,
        detail: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
<<<<<<< HEAD
        operator_user_id = operator_user_id if operator_user_id is not None else operator.get("id") if operator else None
        operator_username = operator_username or (operator.get("username") if operator else None)
=======
        operator_user_id = (
            operator_user_id
            if operator_user_id is not None
            else operator.get("id")
            if operator
            else None
        )
        operator_username = operator_username or (
            operator.get("username") if operator else None
        )
>>>>>>> 98bf8e49 (update)
        operator_role = operator_role or (operator.get("role") if operator else None)

        payload = {
            "module": module,
            "action": action,
            "result": result,
            "message": message or "",
            "operator_user_id": operator_user_id,
            "operator_username": operator_username,
            "operator_role": operator_role,
            "target_type": target_type,
            "target_id": target_id,
            "target_name": target_name,
            "detail": self._sanitize_detail(detail or {}),
            "created_at": self.now_str(),
        }
        return audit_logs_repo.create(payload)

    def list_records(
        self,
        *,
        keyword: Optional[str] = None,
        module: Optional[str] = None,
        action: Optional[str] = None,
        result: Optional[str] = None,
        operator_username: Optional[str] = None,
        operator_role: Optional[str] = None,
<<<<<<< HEAD
=======
        target_name: Optional[str] = None,
>>>>>>> 98bf8e49 (update)
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> list[Dict[str, Any]]:
        rows = audit_logs_repo.list_all()
        keyword_lower = keyword.strip().lower() if keyword else None
<<<<<<< HEAD
=======
        target_name_lower = target_name.strip().lower() if target_name else None
>>>>>>> 98bf8e49 (update)
        output: list[Dict[str, Any]] = []

        for item in rows:
            if module is not None and item.get("module") != module:
                continue
            if action is not None and item.get("action") != action:
                continue
            if result is not None and item.get("result") != result:
                continue
<<<<<<< HEAD
            if operator_username is not None and item.get("operator_username") != operator_username:
                continue
            if operator_role is not None and item.get("operator_role") != operator_role:
                continue
=======
            if (
                operator_username is not None
                and item.get("operator_username") != operator_username
            ):
                continue
            if operator_role is not None and item.get("operator_role") != operator_role:
                continue
            if (
                target_name_lower
                and target_name_lower not in str(item.get("target_name", "")).lower()
            ):
                continue
>>>>>>> 98bf8e49 (update)

            created_at = str(item.get("created_at", ""))
            created_date = created_at[:10] if len(created_at) >= 10 else created_at
            if start_date and created_date < start_date:
                continue
            if end_date and created_date > end_date:
                continue

            if keyword_lower:
                haystacks = [
                    str(item.get("module", "")),
                    str(item.get("action", "")),
                    str(item.get("message", "")),
                    str(item.get("operator_username", "")),
                    str(item.get("target_name", "")),
                    str(item.get("target_type", "")),
                ]
                if keyword_lower not in " ".join(haystacks).lower():
                    continue

            output.append(item)

        output.sort(key=lambda row: int(row.get("id", 0)), reverse=True)
        return output

<<<<<<< HEAD
    def summary(self, records: Optional[Iterable[Dict[str, Any]]] = None) -> Dict[str, Any]:
=======
    def summary(
        self, records: Optional[Iterable[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
>>>>>>> 98bf8e49 (update)
        rows = list(records) if records is not None else self.list_records()
        today_str = datetime.now().strftime("%Y-%m-%d")

        success_count = sum(1 for item in rows if item.get("result") == "success")
        failed_count = sum(1 for item in rows if item.get("result") == "failed")
<<<<<<< HEAD
        today_count = sum(1 for item in rows if str(item.get("created_at", "")).startswith(today_str))
=======
        today_count = sum(
            1 for item in rows if str(item.get("created_at", "")).startswith(today_str)
        )
>>>>>>> 98bf8e49 (update)
        unique_operators = {
            str(item.get("operator_username"))
            for item in rows
            if item.get("operator_username")
        }

<<<<<<< HEAD
        module_distribution = Counter(str(item.get("module", "unknown")) for item in rows)
        action_distribution = Counter(str(item.get("action", "unknown")) for item in rows)
=======
        module_distribution = Counter(
            str(item.get("module", "unknown")) for item in rows
        )
        action_distribution = Counter(
            str(item.get("action", "unknown")) for item in rows
        )
>>>>>>> 98bf8e49 (update)

        return {
            "total_count": len(rows),
            "today_count": today_count,
            "success_count": success_count,
            "failed_count": failed_count,
            "unique_operator_count": len(unique_operators),
            "module_distribution": [
                {"module": key, "count": count}
                for key, count in module_distribution.most_common()
            ],
            "action_distribution": [
                {"action": key, "count": count}
                for key, count in action_distribution.most_common()
            ],
        }

<<<<<<< HEAD
=======
    def export_records(
        self,
        *,
        keyword: Optional[str] = None,
        module: Optional[str] = None,
        action: Optional[str] = None,
        result: Optional[str] = None,
        operator_username: Optional[str] = None,
        operator_role: Optional[str] = None,
        target_name: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Path:
        rows = self.list_records(
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
        filename = f"audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        output_path = REPORTS_DIR / filename
        return export_audit_log_records(rows, output_path)

>>>>>>> 98bf8e49 (update)

audit_log_service = AuditLogService()
