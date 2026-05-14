from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Sequence
from uuid import uuid4

from app.core.config import (
    ALLOWED_IMAGE_SUFFIXES,
    ATTACK_SAMPLES_DIR,
    DATETIME_FORMAT,
    REPORTS_DIR,
)
from app.core.exceptions import AppException
from app.services.face_engine import face_engine
<<<<<<< HEAD
from app.services.model_liveness_engine import model_liveness_engine as liveness_engine
=======
from app.services.liveness_engine import liveness_engine
>>>>>>> 98bf8e49 (update)
from app.storage.excel_exporter import export_security_test_records
from app.storage.repositories import security_test_records_repo


class SecurityTestService:
<<<<<<< HEAD
=======
    _TEST_TYPE_LABELS = {
        "real_person": "真人",
        "printed_photo": "打印照片",
        "screen_photo": "屏幕照片",
        "screen_video": "屏幕视频",
    }

>>>>>>> 98bf8e49 (update)
    @staticmethod
    def now_str() -> str:
        return datetime.now().strftime(DATETIME_FORMAT)

    @staticmethod
    def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
        normalized = dict(record)
        normalized.setdefault("frame_count", 1)
        normalized.setdefault("valid_frame_count", 1)
<<<<<<< HEAD
        normalized.setdefault("confidence", 0.5)
        normalized.setdefault("threshold", 0.5)
        normalized.setdefault("liveness_mode", "unknown")
        normalized.setdefault("remark", None)
        normalized.setdefault("operator_username", None)
        normalized.setdefault("sample_path", None)
=======
        normalized.setdefault("confidence", normalized.get("confidence", normalized.get("spoof_confidence", 0.5)))
        normalized.setdefault("threshold", normalized.get("threshold", normalized.get("spoof_real_threshold", 0.58)))
        normalized.setdefault("liveness_mode", normalized.get("liveness_mode", normalized.get("spoof_model_name", "passive_anti_spoof")))
        normalized.setdefault("verification_mode", normalized.get("verification_mode", normalized.get("liveness_mode", "passive_anti_spoof")))
        normalized.setdefault("remark", None)
        normalized.setdefault("operator_username", None)
        normalized.setdefault("sample_path", None)
        normalized.setdefault("liveness_result", normalized.get("liveness_result", normalized.get("result", "unknown")))
        normalized.setdefault("liveness_score", normalized.get("liveness_score", normalized.get("score")))
        normalized.setdefault("liveness_confidence", normalized.get("confidence"))
        normalized.setdefault("challenge_confidence", normalized.get("challenge_confidence"))
        normalized.setdefault("challenge_result", "skipped" if not normalized.get("challenge_used") else normalized.get("challenge_result", "uncertain"))
        normalized.setdefault("challenge_action", None)
        normalized.setdefault("challenge_action_label", None)
        normalized.setdefault("challenge_prompt", None)
        normalized.setdefault("challenge_score", normalized.get("challenge_score"))
        normalized.setdefault("challenge_threshold", normalized.get("challenge_threshold"))
        normalized.setdefault("challenge_reason", None)
        normalized.setdefault("challenge_details", None)
        normalized.setdefault("spoof_result", normalized.get("spoof_result", normalized.get("liveness_result", "unknown")))
        normalized.setdefault("spoof_score", normalized.get("spoof_score", normalized.get("liveness_score")))
        normalized.setdefault("spoof_confidence", normalized.get("spoof_confidence", normalized.get("confidence")))
        normalized.setdefault("spoof_attack_type", None)
        normalized.setdefault("spoof_model_name", normalized.get("spoof_model_name", normalized.get("liveness_mode")))
        normalized.setdefault("spoof_reason", normalized.get("spoof_reason", normalized.get("challenge_reason")))
        normalized.setdefault("model_score", None)
        normalized.setdefault("heuristic_score", None)
        normalized.setdefault("real_frame_count", None)
        normalized.setdefault("real_frame_ratio", None)
        normalized.setdefault("static_score", None)
        normalized.setdefault("temporal", {})
        normalized.setdefault("model_predictions", [])
        normalized.setdefault("accepted_frame_count", None)
        normalized.setdefault("rejected_frame_count", None)
        normalized.setdefault("quality_insufficient", False)
        normalized.setdefault("uncertain", False)
        normalized.setdefault("frame_debug", [])
        normalized.setdefault("challenge_required", False)
        normalized.setdefault("challenge_used", False)
        normalized.setdefault("attack_suspected", False)
        normalized.setdefault("final_decision", None)
        normalized.setdefault("challenge_id", None)
>>>>>>> 98bf8e49 (update)
        return normalized

    @staticmethod
    def _validate_filename(filename: str) -> str:
        suffix = Path(filename).suffix.lower()
        if suffix not in ALLOWED_IMAGE_SUFFIXES:
            raise AppException(
                message=f"不支持的图片格式，仅支持: {sorted(ALLOWED_IMAGE_SUFFIXES)}",
                code=4002,
                status_code=400,
            )
        return suffix

    @staticmethod
    def _result_label(result: str) -> str:
<<<<<<< HEAD
        return "通过" if result == "real" else "拦截"

    @staticmethod
    def _test_type_label(test_type: str) -> str:
        mapping = {
            "live_sample": "实时活体",
            "photo_attack": "照片攻击",
            "video_attack": "视频攻击",
        }
        return mapping.get(test_type, test_type)
=======
        if result == "real":
            return "通过"
        if result == "fake":
            return "未通过"
        if result == "uncertain":
            return "待重采样"
        return result

    def _test_type_label(self, test_type: str) -> str:
        return self._TEST_TYPE_LABELS.get(test_type, test_type)
>>>>>>> 98bf8e49 (update)

    def list_records(
        self,
        *,
        keyword: Optional[str] = None,
        test_type: Optional[str] = None,
        result: Optional[str] = None,
        liveness_mode: Optional[str] = None,
        operator_username: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> list[Dict[str, Any]]:
        records = [self.normalize_record(item) for item in security_test_records_repo.list_all()]
        keyword_lower = keyword.strip().lower() if keyword else None
        output: list[Dict[str, Any]] = []

        for item in records:
            if test_type is not None and item.get("test_type") != test_type:
                continue
            if result is not None and item.get("result") != result:
                continue
            if liveness_mode is not None and item.get("liveness_mode") != liveness_mode:
                continue
            if operator_username is not None and item.get("operator_username") != operator_username:
                continue

            created_at = str(item.get("created_at", ""))
            created_date = created_at[:10] if len(created_at) >= 10 else created_at
            if start_date and created_date < start_date:
                continue
            if end_date and created_date > end_date:
                continue

            if keyword_lower:
                haystacks = [
                    str(item.get("test_type", "")),
                    str(item.get("result", "")),
                    str(item.get("liveness_mode", "")),
                    str(item.get("operator_username", "")),
                    str(item.get("remark", "")),
<<<<<<< HEAD
=======
                    str(item.get("challenge_action", "")),
>>>>>>> 98bf8e49 (update)
                ]
                if keyword_lower not in " ".join(haystacks).lower():
                    continue

            output.append(item)

        output.sort(key=lambda x: int(x.get("id", 0)), reverse=True)
        return output

    def summary(
        self,
        *,
        keyword: Optional[str] = None,
        test_type: Optional[str] = None,
        result: Optional[str] = None,
        liveness_mode: Optional[str] = None,
        operator_username: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        records = self.list_records(
            keyword=keyword,
            test_type=test_type,
            result=result,
            liveness_mode=liveness_mode,
            operator_username=operator_username,
            start_date=start_date,
            end_date=end_date,
        )
        today_str = datetime.now().strftime("%Y-%m-%d")

        total_count = len(records)
        real_count = sum(1 for item in records if item.get("result") == "real")
        fake_count = sum(1 for item in records if item.get("result") == "fake")
<<<<<<< HEAD
        today_count = sum(1 for item in records if str(item.get("created_at", "")).startswith(today_str))
        avg_score = round(
            sum(float(item.get("score", 0.0) or 0.0) for item in records) / total_count,
            6,
        ) if total_count else 0.0
        avg_confidence = round(
            sum(float(item.get("confidence", 0.0) or 0.0) for item in records) / total_count,
            6,
        ) if total_count else 0.0

        test_type_counter = Counter(str(item.get("test_type", "unknown")) for item in records)
        result_counter = Counter(str(item.get("result", "unknown")) for item in records)
        mode_counter = Counter(str(item.get("liveness_mode", "unknown")) for item in records)
=======
        uncertain_count = sum(1 for item in records if item.get("result") == "uncertain")
        today_count = sum(1 for item in records if str(item.get("created_at", "")).startswith(today_str))
        avg_score = (
            round(sum(float(item.get("score", 0.0) or 0.0) for item in records) / total_count, 6)
            if total_count
            else 0.0
        )
        avg_confidence = (
            round(sum(float(item.get("confidence", 0.0) or 0.0) for item in records) / total_count, 6)
            if total_count
            else 0.0
        )

        test_type_counter = Counter(str(item.get("test_type", "unknown")) for item in records)
        result_counter = Counter(str(item.get("result", "unknown")) for item in records)
        mode_counter = Counter(str(item.get("verification_mode", "unknown")) for item in records)
        action_counter = Counter(str(item.get("challenge_action", "none")) for item in records if item.get("challenge_action"))
>>>>>>> 98bf8e49 (update)

        score_sum_by_type: defaultdict[str, float] = defaultdict(float)
        count_by_type: defaultdict[str, int] = defaultdict(int)
        for item in records:
            key = str(item.get("test_type", "unknown"))
            score_sum_by_type[key] += float(item.get("score", 0.0) or 0.0)
            count_by_type[key] += 1

        type_breakdown = []
        for key, count in test_type_counter.items():
<<<<<<< HEAD
            real_hits = sum(
                1
                for item in records
                if item.get("test_type") == key and item.get("result") == "real"
            )
            fake_hits = sum(
                1
                for item in records
                if item.get("test_type") == key and item.get("result") == "fake"
            )
=======
            real_hits = sum(1 for item in records if item.get("test_type") == key and item.get("result") == "real")
            fake_hits = sum(1 for item in records if item.get("test_type") == key and item.get("result") == "fake")
>>>>>>> 98bf8e49 (update)
            type_breakdown.append(
                {
                    "test_type": key,
                    "label": self._test_type_label(key),
                    "count": count,
                    "real_count": real_hits,
                    "fake_count": fake_hits,
                    "average_score": round(score_sum_by_type[key] / count_by_type[key], 6)
                    if count_by_type[key]
                    else 0.0,
                }
            )

<<<<<<< HEAD
        daily_counter: dict[str, dict[str, int]] = defaultdict(
            lambda: {"real": 0, "fake": 0, "total": 0}
        )
=======
        daily_counter: dict[str, dict[str, int]] = defaultdict(lambda: {"real": 0, "fake": 0, "uncertain": 0, "total": 0})
>>>>>>> 98bf8e49 (update)
        for item in records:
            created_at = str(item.get("created_at", ""))
            day = created_at[:10] if len(created_at) >= 10 else created_at
            if not day:
                continue
            row = daily_counter[day]
            row["total"] += 1
            row[str(item.get("result", "unknown"))] = row.get(str(item.get("result", "unknown")), 0) + 1

        daily_trend = [
            {"date": key, **value}
            for key, value in sorted(daily_counter.items(), key=lambda item: item[0], reverse=True)
        ]

        return {
            "dashboard": {
                "total_count": total_count,
                "today_count": today_count,
                "real_count": real_count,
                "fake_count": fake_count,
<<<<<<< HEAD
=======
                "uncertain_count": uncertain_count,
>>>>>>> 98bf8e49 (update)
                "average_score": avg_score,
                "average_confidence": avg_confidence,
            },
            "test_type_distribution": [
                {"test_type": key, "label": self._test_type_label(key), "count": count}
                for key, count in test_type_counter.most_common()
            ],
            "result_distribution": [
                {"result": key, "label": self._result_label(key), "count": count}
                for key, count in result_counter.most_common()
            ],
            "mode_distribution": [
<<<<<<< HEAD
                {"liveness_mode": key, "count": count}
                for key, count in mode_counter.most_common()
            ],
=======
                {"verification_mode": key, "count": count}
                for key, count in mode_counter.most_common()
            ],
            "action_distribution": [
                {"challenge_action": key, "count": count}
                for key, count in action_counter.most_common()
            ],
            "attack_distribution": [
                {"attack_type": key, "count": count}
                for key, count in action_counter.most_common()
            ],
>>>>>>> 98bf8e49 (update)
            "type_breakdown": sorted(type_breakdown, key=lambda item: item["count"], reverse=True),
            "daily_trend": daily_trend,
        }

    def export_records(
        self,
        *,
        keyword: Optional[str] = None,
        test_type: Optional[str] = None,
        result: Optional[str] = None,
        liveness_mode: Optional[str] = None,
        operator_username: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Path:
        rows = self.list_records(
            keyword=keyword,
            test_type=test_type,
            result=result,
            liveness_mode=liveness_mode,
            operator_username=operator_username,
            start_date=start_date,
            end_date=end_date,
        )
        filename = f"security_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        output_path = REPORTS_DIR / filename
        return export_security_test_records(rows, output_path)

<<<<<<< HEAD
=======
    @staticmethod
    def _cleanup_saved_frames(saved_frames: Sequence[tuple[Path, str]]) -> None:
        for frame_path, _ in saved_frames:
            if frame_path.exists():
                frame_path.unlink(missing_ok=True)

>>>>>>> 98bf8e49 (update)
    def run_liveness_test(
        self,
        *,
        frame_items: Sequence[tuple[str, bytes]],
        test_type: str,
        remark: str | None,
        operator: Dict[str, Any],
<<<<<<< HEAD
    ) -> Dict[str, Any]:
        if not frame_items:
            raise AppException(message="至少需要上传 1 帧图片", code=4003, status_code=400)
        if test_type not in {"live_sample", "photo_attack", "video_attack"}:
            raise AppException(
                message="test_type 仅支持 live_sample/photo_attack/video_attack",
                code=4226,
                status_code=422,
            )

=======
        challenge_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not frame_items:
            raise AppException(message="至少需要上传 1 帧图片", code=4003, status_code=400)
        valid_types = {"real_person", "printed_photo", "screen_photo", "screen_video"}
        if test_type not in valid_types:
            raise AppException(message="test_type 不合法", code=4226, status_code=422)
>>>>>>> 98bf8e49 (update)
        session_id = uuid4().hex
        saved_frames: list[tuple[Path, str]] = []
        validated_items: list[tuple[str, bytes, str]] = []
        for filename, file_bytes in frame_items:
            if not file_bytes:
                raise AppException(message="上传的图片为空", code=4003, status_code=400)
            suffix = self._validate_filename(filename or "frame.png")
            validated_items.append((filename, file_bytes, suffix))

        for index, (_, file_bytes, suffix) in enumerate(validated_items, start=1):
            unique_name = f"security_{session_id}_{index:02d}{suffix}"
            save_path = ATTACK_SAMPLES_DIR / unique_name
            save_path.write_bytes(file_bytes)
            saved_frames.append((save_path, f"uploads/attack_samples/{unique_name}"))

        valid_frames: list[tuple[Path, str, Dict[str, Any]]] = []
        frame_errors: list[str] = []
<<<<<<< HEAD
        minimum_valid_frames = 3 if len(saved_frames) >= 3 else 1
=======
        minimum_valid_frames = 4 if len(saved_frames) >= 4 else 1
>>>>>>> 98bf8e49 (update)

        try:
            for frame_path, frame_relpath in saved_frames:
                try:
                    result = face_engine.extract_single_face_embedding(frame_path)
                    valid_frames.append((frame_path, frame_relpath, result))
                except Exception as exc:
                    frame_errors.append(str(exc))

            if len(valid_frames) < minimum_valid_frames:
                raise AppException(
                    message="安全测试样本中的有效单人脸帧数量不足",
                    code=4227,
                    status_code=422,
                    data={
                        "uploaded_frame_count": len(saved_frames),
                        "valid_frame_count": len(valid_frames),
                        "frame_errors": frame_errors,
                    },
                )

            liveness = liveness_engine.evaluate_sequence(
                [frame_path for frame_path, _, _ in valid_frames],
                [item["bbox"] for _, _, item in valid_frames],
<<<<<<< HEAD
            )
        except Exception:
            for frame_path, _ in saved_frames:
                if frame_path.exists():
                    frame_path.unlink(missing_ok=True)
            raise

        primary_relpath = saved_frames[len(saved_frames) // 2][1]
=======
                [item.get("landmarks") for _, _, item in valid_frames],
                challenge_id=challenge_id,
                purpose="security_test",
                operator_username=operator.get("username"),
            )
        except Exception:
            self._cleanup_saved_frames(saved_frames)
            raise

        primary_path, primary_relpath, primary_probe = max(
            valid_frames,
            key=lambda item: float(item[2].get("det_score", 0.0) or 0.0),
        )

>>>>>>> 98bf8e49 (update)
        record = security_test_records_repo.create(
            {
                "test_type": test_type,
                "sample_path": primary_relpath,
                "frame_count": len(saved_frames),
                "valid_frame_count": len(valid_frames),
                "result": liveness["result"],
                "score": liveness["score"],
                "confidence": liveness["confidence"],
                "threshold": liveness["threshold"],
<<<<<<< HEAD
                "liveness_mode": liveness["mode"],
                "created_at": self.now_str(),
                "remark": remark,
                "operator_username": operator.get("username"),
=======
                "liveness_mode": liveness["verification_mode"],
                "verification_mode": liveness["verification_mode"],
                "remark": remark,
                "operator_username": operator.get("username"),
                "liveness_result": liveness["result"],
                "liveness_score": liveness["score"],
                "liveness_confidence": liveness["confidence"],
                "challenge_result": liveness["challenge_result"],
                "challenge_action": liveness["challenge_action"],
                "challenge_action_label": liveness["challenge_action_label"],
                "challenge_prompt": liveness["challenge_prompt"],
                "challenge_score": liveness["challenge_score"],
                "challenge_confidence": liveness.get("challenge_confidence", liveness.get("confidence")),
                "challenge_threshold": liveness["challenge_threshold"],
                "challenge_reason": liveness["challenge_reason"],
                "challenge_details": liveness.get("challenge_details"),
                "challenge_id": liveness.get("challenge_id"),
                "spoof_result": liveness.get("spoof_result"),
                "spoof_score": liveness.get("spoof_score"),
                "spoof_confidence": liveness.get("spoof_confidence"),
                "spoof_attack_type": liveness.get("spoof_attack_type"),
                "spoof_model_name": liveness.get("spoof_model_name"),
                "spoof_reason": liveness.get("spoof_reason"),
                "model_score": liveness.get("model_score"),
                "heuristic_score": liveness.get("heuristic_score"),
                "real_frame_count": liveness.get("real_frame_count"),
                "real_frame_ratio": liveness.get("real_frame_ratio"),
                "static_score": liveness.get("static_score"),
                "temporal": liveness.get("temporal", {}),
                "model_predictions": liveness.get("model_predictions", []),
                "accepted_frame_count": liveness.get("accepted_frame_count"),
                "rejected_frame_count": liveness.get("rejected_frame_count"),
                "quality_insufficient": liveness.get("quality_insufficient", False),
                "uncertain": liveness.get("result") == "uncertain",
                "attack_suspected": liveness["result"] == "fake",
                "final_decision": "allow" if liveness["result"] == "real" else ("retry" if liveness["result"] == "uncertain" else "block"),
                "challenge_required": False,
                "challenge_used": liveness.get("challenge_used", False),
                "created_at": self.now_str(),
                "frame_debug": liveness.get("frame_debug", []),
>>>>>>> 98bf8e49 (update)
            }
        )

        return {
            "record_id": record["id"],
            "test_type": test_type,
            "sample_path": primary_relpath,
            "frame_count": len(saved_frames),
            "valid_frame_count": len(valid_frames),
            "result": liveness["result"],
            "score": liveness["score"],
            "confidence": liveness["confidence"],
            "threshold": liveness["threshold"],
<<<<<<< HEAD
            "liveness_mode": liveness["mode"],
            "temporal": liveness["temporal"],
=======
            "liveness_mode": liveness["verification_mode"],
            "verification_mode": liveness["verification_mode"],
            "liveness_result": liveness["result"],
            "liveness_score": liveness["score"],
            "liveness_confidence": liveness["confidence"],
            "challenge_result": liveness["challenge_result"],
            "challenge_action": liveness["challenge_action"],
            "challenge_action_label": liveness["challenge_action_label"],
            "challenge_prompt": liveness["challenge_prompt"],
            "challenge_score": liveness["challenge_score"],
            "challenge_confidence": liveness.get("challenge_confidence", liveness.get("confidence")),
            "challenge_threshold": liveness["challenge_threshold"],
            "challenge_reason": liveness["challenge_reason"],
            "challenge_details": liveness.get("challenge_details"),
            "challenge_id": liveness.get("challenge_id"),
            "spoof_result": liveness.get("spoof_result"),
            "spoof_score": liveness.get("spoof_score"),
            "spoof_confidence": liveness.get("spoof_confidence"),
            "spoof_attack_type": liveness.get("spoof_attack_type"),
            "spoof_model_name": liveness.get("spoof_model_name"),
            "spoof_reason": liveness.get("spoof_reason"),
            "model_score": liveness.get("model_score"),
            "heuristic_score": liveness.get("heuristic_score"),
            "real_frame_count": liveness.get("real_frame_count"),
            "real_frame_ratio": liveness.get("real_frame_ratio"),
            "static_score": liveness.get("static_score"),
            "temporal": liveness.get("temporal", {}),
            "model_predictions": liveness.get("model_predictions", []),
            "accepted_frame_count": liveness.get("accepted_frame_count"),
            "rejected_frame_count": liveness.get("rejected_frame_count"),
            "quality_insufficient": liveness.get("quality_insufficient", False),
            "uncertain": liveness.get("result") == "uncertain",
            "frame_debug": liveness.get("frame_debug", []),
            "challenge_required": False,
            "challenge_used": liveness.get("challenge_used", False),
            "attack_suspected": liveness["result"] == "fake",
            "reason": liveness["reason"],
>>>>>>> 98bf8e49 (update)
            "created_at": record["created_at"],
        }


security_test_service = SecurityTestService()
