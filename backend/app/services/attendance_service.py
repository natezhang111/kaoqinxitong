from __future__ import annotations

from datetime import datetime, time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence
from uuid import uuid4

from app.core.config import (
    ALLOWED_IMAGE_SUFFIXES,
    ATTENDANCE_UPLOAD_DIR,
    DATETIME_FORMAT,
    FACE_MATCH_THRESHOLD,
    FEATURES_DIR,
    REPORTS_DIR,
)
from app.core.exceptions import AppException
from app.services.emotion_engine import emotion_engine
from app.services.emotion_service import emotion_service
from app.services.face_engine import face_engine
<<<<<<< HEAD
from app.services.model_liveness_engine import model_liveness_engine as liveness_engine
=======
from app.services.liveness_engine import liveness_engine
>>>>>>> 98bf8e49 (update)
from app.storage.excel_exporter import export_attendance_records
from app.storage.repositories import attendance_repo, students_repo


def _parse_date_start(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise AppException(message="开始日期格式应为 YYYY-MM-DD", code=4221, status_code=422)


def _parse_date_end(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date()
        return datetime.combine(parsed, time.max.replace(microsecond=0))
    except ValueError:
        raise AppException(message="结束日期格式应为 YYYY-MM-DD", code=4222, status_code=422)


class AttendanceService:
    def now_str(self) -> str:
        return datetime.now().strftime(DATETIME_FORMAT)

    @staticmethod
<<<<<<< HEAD
=======
    def _build_note(liveness: Dict[str, Any], *, matched: bool) -> str:
        if liveness.get("challenge_used"):
            return "被动活体与随机动作校验通过，且人脸识别成功" if matched else "被动活体与随机动作校验通过，但未匹配到已知学生"
        return "被动活体校验通过，且人脸识别成功" if matched else "被动活体校验通过，但未匹配到已知学生"

    @staticmethod
>>>>>>> 98bf8e49 (update)
    def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
        normalized = dict(record)
        normalized.setdefault("capture_mode", "manual")
        normalized.setdefault("threshold", FACE_MATCH_THRESHOLD)
<<<<<<< HEAD
        normalized.setdefault("liveness_result", "unknown")
        normalized.setdefault("liveness_score", None)
        normalized.setdefault("liveness_mode", "unknown")
=======
        normalized.setdefault("liveness_result", normalized.get("liveness_result", normalized.get("spoof_result", "unknown")))
        normalized.setdefault("liveness_score", normalized.get("liveness_score", normalized.get("spoof_score")))
        normalized.setdefault("liveness_confidence", normalized.get("liveness_confidence", normalized.get("spoof_confidence")))
        normalized.setdefault("liveness_mode", normalized.get("liveness_mode", normalized.get("spoof_model_name", "passive_anti_spoof")))
        normalized.setdefault("verification_mode", normalized.get("verification_mode", normalized.get("liveness_mode", "passive_anti_spoof")))
>>>>>>> 98bf8e49 (update)
        normalized.setdefault("frame_count", 1)
        normalized.setdefault("valid_frame_count", 1)
        normalized.setdefault("emotion", None)
        normalized.setdefault("emotion_score", None)
<<<<<<< HEAD
        normalized.setdefault("operator_role", None)
        normalized.setdefault("operator_username", None)
=======
        normalized.setdefault("emotion_mode", None)
        normalized.setdefault("operator_role", None)
        normalized.setdefault("operator_username", None)
        normalized.setdefault("challenge_result", "skipped" if not normalized.get("challenge_used") else normalized.get("challenge_result", "uncertain"))
        normalized.setdefault("challenge_score", normalized.get("challenge_score"))
        normalized.setdefault("challenge_confidence", normalized.get("challenge_confidence"))
        normalized.setdefault("challenge_action", None)
        normalized.setdefault("challenge_action_label", None)
        normalized.setdefault("challenge_prompt", None)
        normalized.setdefault("challenge_threshold", None)
        normalized.setdefault("challenge_reason", None)
        normalized.setdefault("challenge_details", None)
        normalized.setdefault("spoof_result", normalized.get("liveness_result", "unknown"))
        normalized.setdefault("spoof_score", normalized.get("liveness_score"))
        normalized.setdefault("spoof_confidence", normalized.get("liveness_confidence"))
        normalized.setdefault("spoof_attack_type", None)
        normalized.setdefault("spoof_model_name", normalized.get("spoof_model_name", normalized.get("liveness_mode")))
        normalized.setdefault("spoof_reason", normalized.get("spoof_reason", normalized.get("reason")))
        normalized.setdefault("spoof_real_threshold", None)
        normalized.setdefault("spoof_fake_threshold", None)
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
        normalized.setdefault("challenge_id", None)
        normalized.setdefault("final_decision", None)
        normalized.setdefault("reason", normalized.get("reason", normalized.get("challenge_reason")))
>>>>>>> 98bf8e49 (update)
        return normalized

    def validate_image_filename(self, filename: Optional[str]) -> str:
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

    @staticmethod
    def attendance_image_relpath(filename: str) -> str:
        return f"uploads/attendance/{filename}"

<<<<<<< HEAD
    def _save_frame_items(
        self, frame_items: Sequence[tuple[str, bytes]]
    ) -> list[tuple[Path, str]]:
=======
    def _save_frame_items(self, frame_items: Sequence[tuple[str, bytes]]) -> list[tuple[Path, str]]:
>>>>>>> 98bf8e49 (update)
        saved: list[tuple[Path, str]] = []
        session_id = uuid4().hex
        validated_items: list[tuple[str, bytes, str]] = []
        for filename, file_bytes in frame_items:
            suffix = self.validate_image_filename(filename)
            validated_items.append((filename, file_bytes, suffix))

        for index, (_, file_bytes, suffix) in enumerate(validated_items, start=1):
            unique_name = f"attendance_{session_id}_{index:02d}{suffix}"
            save_path = ATTENDANCE_UPLOAD_DIR / unique_name
            save_path.write_bytes(file_bytes)
            saved.append((save_path, self.attendance_image_relpath(unique_name)))
        return saved

<<<<<<< HEAD
=======
    @staticmethod
    def _cleanup_saved_frames(saved_frames: Sequence[tuple[Path, str]]) -> None:
        for frame_path, _ in saved_frames:
            if frame_path.exists():
                frame_path.unlink(missing_ok=True)

>>>>>>> 98bf8e49 (update)
    def load_active_students_with_features(self) -> List[tuple[Dict[str, Any], Path]]:
        students = students_repo.list_active_students()
        valid_students: List[tuple[Dict[str, Any], Path]] = []

        for student in students:
            feature_relpath = student.get("face_feature_path")
            if not feature_relpath:
                continue

            feature_path = FEATURES_DIR / Path(str(feature_relpath)).name
            if not feature_path.exists():
                continue

            valid_students.append((student, feature_path))

        return valid_students

    def list_records(
        self,
        *,
        current_user: Dict[str, Any],
        keyword: Optional[str] = None,
        class_name: Optional[str] = None,
        status: Optional[str] = None,
        capture_mode: Optional[str] = None,
        liveness_result: Optional[str] = None,
        emotion: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        records = attendance_repo.list_all()
        result: List[Dict[str, Any]] = []
        keyword_lower = keyword.strip().lower() if keyword else None
        dt_start = _parse_date_start(start_date)
        dt_end = _parse_date_end(end_date)

        for raw_item in records:
            item = self.normalize_record(raw_item)
            if current_user.get("role") == "student":
                student_id = current_user.get("student_id")
                if student_id is None or item.get("student_id") != student_id:
                    continue

            if class_name and item.get("class_name") != class_name:
                continue
            if status and item.get("status") != status:
                continue
            if capture_mode and item.get("capture_mode") != capture_mode:
                continue
            if liveness_result and item.get("liveness_result") != liveness_result:
                continue
            if emotion and item.get("emotion") != emotion:
                continue

            if keyword_lower:
                student_no = str(item.get("student_no", "")).lower()
                student_name = str(item.get("student_name", "")).lower()
                if keyword_lower not in student_no and keyword_lower not in student_name:
                    continue

            created_at = item.get("created_at")
            if created_at:
                try:
                    created_dt = datetime.strptime(created_at, DATETIME_FORMAT)
                except ValueError:
                    created_dt = None
                if created_dt is not None:
                    if dt_start and created_dt < dt_start:
                        continue
                    if dt_end and created_dt > dt_end:
                        continue

            result.append(item)

        result.sort(key=lambda x: x.get("id", 0), reverse=True)
        return result

    def get_record(self, record_id: int, current_user: Dict[str, Any]) -> Dict[str, Any]:
        raw_record = attendance_repo.get_by_id(record_id)
        record = self.normalize_record(raw_record) if raw_record is not None else None
        if record is None:
            raise AppException(message="考勤记录不存在", code=4041, status_code=404)

        if current_user.get("role") == "student":
            student_id = current_user.get("student_id")
            if student_id is None or record.get("student_id") != student_id:
                raise AppException(message="无权查看该考勤记录", code=4033, status_code=403)

        return record

    def export_records(
        self,
        *,
        current_user: Dict[str, Any],
        keyword: Optional[str] = None,
        class_name: Optional[str] = None,
        status: Optional[str] = None,
        capture_mode: Optional[str] = None,
        liveness_result: Optional[str] = None,
        emotion: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Path:
        records = self.list_records(
            current_user=current_user,
            keyword=keyword,
            class_name=class_name,
            status=status,
            capture_mode=capture_mode,
            liveness_result=liveness_result,
            emotion=emotion,
            start_date=start_date,
            end_date=end_date,
        )
        filename = f"attendance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        output_path = REPORTS_DIR / filename
        return export_attendance_records(records, output_path)

    @staticmethod
    def _average_embeddings(embeddings: Sequence[Any]):
        import numpy as np

        stacked = np.stack(embeddings, axis=0).astype(np.float32)
        mean_embedding = np.mean(stacked, axis=0)
        norm = float(np.linalg.norm(mean_embedding))
        if norm <= 1e-12:
            raise AppException(message="连续帧特征向量无效", code=5008, status_code=500)
        return mean_embedding / norm

<<<<<<< HEAD
=======
    def _collect_valid_frames(
        self,
        saved_frames: Sequence[tuple[Path, str]],
    ) -> tuple[list[tuple[Path, str, Dict[str, Any]]], list[str]]:
        valid_frames: list[tuple[Path, str, Dict[str, Any]]] = []
        frame_errors: list[str] = []
        for frame_path, frame_relpath in saved_frames:
            try:
                probe_result = face_engine.extract_single_face_embedding(frame_path)
                valid_frames.append((frame_path, frame_relpath, probe_result))
            except Exception as exc:
                frame_errors.append(str(exc))
        return valid_frames, frame_errors

    @staticmethod
    def _select_primary_frame(
        frames: Sequence[tuple[Path, str, Dict[str, Any]]],
    ) -> tuple[Path, str, Dict[str, Any]]:
        if not frames:
            raise AppException(message="没有可用于展示的有效人脸帧", code=4225, status_code=422)
        ranked_frames = [
            (
                index,
                item,
                float(item[2].get("det_score", 0.0) or 0.0),
                abs((len(frames) // 2) - index),
            )
            for index, item in enumerate(frames)
        ]
        ranked_frames.sort(key=lambda item: (item[2], -item[3]), reverse=True)
        return ranked_frames[0][1]

    @staticmethod
    def _analyze_emotion_safe(
        image_path: Path,
        probe_result: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        try:
            return emotion_engine.analyze_face(
                image_path,
                probe_result.get("bbox"),
                probe_result.get("landmarks"),
            )
        except Exception:
            return None

    @staticmethod
    def _build_response_payload(
        *,
        status: str,
        matched: bool,
        record_id: Optional[int],
        student: Optional[Dict[str, Any]],
        image_path: Optional[str],
        capture_mode: str,
        match_score: float,
        bbox: Optional[Sequence[float]],
        det_score: Optional[float],
        frame_count: int,
        valid_frame_count: int,
        emotion_result: Optional[Dict[str, Any]],
        liveness: Dict[str, Any],
        threshold: float,
    ) -> Dict[str, Any]:
        challenge_used = bool(liveness.get("challenge_used", False))
        payload = {
            "matched": matched,
            "student_id": None if student is None else student.get("id"),
            "student_no": None if student is None else student.get("student_no"),
            "student_name": None if student is None else student.get("name"),
            "class_name": None if student is None else student.get("class_name"),
            "image_path": image_path,
            "capture_mode": capture_mode,
            "match_score": round(float(match_score), 6),
            "threshold": threshold,
            "status": status,
            "record_id": record_id,
            "bbox": bbox,
            "det_score": det_score,
            "liveness_result": liveness["result"],
            "liveness_score": liveness["score"],
            "liveness_confidence": liveness["confidence"],
            "liveness_threshold": liveness.get("threshold"),
            "liveness_mode": liveness["verification_mode"],
            "verification_mode": liveness["verification_mode"],
            "spoof_result": liveness.get("spoof_result"),
            "spoof_score": liveness.get("spoof_score"),
            "spoof_confidence": liveness.get("spoof_confidence"),
            "spoof_attack_type": liveness.get("spoof_attack_type"),
            "spoof_model_name": liveness.get("spoof_model_name"),
            "spoof_reason": liveness.get("spoof_reason"),
            "spoof_real_threshold": liveness.get("spoof_real_threshold"),
            "spoof_fake_threshold": liveness.get("spoof_fake_threshold"),
            "model_score": liveness.get("model_score"),
            "heuristic_score": liveness.get("heuristic_score"),
            "real_frame_count": liveness.get("real_frame_count"),
            "real_frame_ratio": liveness.get("real_frame_ratio"),
            "static_score": liveness.get("static_score"),
            "temporal": liveness.get("temporal", {}),
            "model_predictions": liveness.get("model_predictions", []),
            "live_score": liveness.get("passive_score", liveness["score"]),
            "live_score_min": liveness.get("passive_score", liveness["score"]),
            "live_score_median": liveness.get("passive_score", liveness["score"]),
            "live_score_p25": liveness.get("passive_score", liveness["score"]),
            "print_attack_score": next(
                (
                    indicator.get("score")
                    for indicator in liveness.get("risk_indicators", [])
                    if indicator.get("type") == "print_attack"
                ),
                None,
            ),
            "replay_attack_score": next(
                (
                    indicator.get("score")
                    for indicator in liveness.get("risk_indicators", [])
                    if indicator.get("type") == "replay_attack"
                ),
                None,
            ),
            "frame_count": frame_count,
            "valid_frame_count": valid_frame_count,
            "accepted_frame_count": liveness.get("accepted_frame_count"),
            "rejected_frame_count": liveness.get("rejected_frame_count"),
            "quality_insufficient": liveness.get("quality_insufficient", False),
            "uncertain": liveness.get("result") == "uncertain",
            "frame_debug": liveness.get("frame_debug", []),
            "emotion": None if emotion_result is None else emotion_result["emotion"],
            "emotion_score": None if emotion_result is None else emotion_result["score"],
            "emotion_mode": None if emotion_result is None else emotion_result.get("mode"),
            "challenge_required": False,
            "challenge_used": challenge_used,
            "attack_suspected": liveness["result"] == "fake",
            "challenge_id": liveness.get("challenge_id"),
            "challenge_action": liveness.get("challenge_action"),
            "challenge_action_label": liveness.get("challenge_action_label"),
            "challenge_prompt": liveness.get("challenge_prompt"),
            "challenge_result": liveness.get("challenge_result", "skipped"),
            "challenge_score": liveness.get("challenge_score"),
            "challenge_confidence": liveness.get("challenge_confidence", liveness.get("confidence")),
            "challenge_threshold": liveness.get("challenge_threshold"),
            "challenge_reason": liveness.get("challenge_reason"),
            "challenge_details": liveness.get("challenge_details"),
            "final_decision": "allow" if liveness["result"] == "real" else ("retry" if liveness["result"] == "uncertain" else "block"),
            "reason": liveness["reason"],
        }
        return payload

>>>>>>> 98bf8e49 (update)
    def recognize_attendance(
        self,
        *,
        frame_items: Sequence[tuple[str, bytes]],
        capture_mode: str,
        current_user: Dict[str, Any],
<<<<<<< HEAD
=======
        challenge_id: Optional[str] = None,
>>>>>>> 98bf8e49 (update)
    ) -> Dict[str, Any]:
        if not frame_items:
            raise AppException(message="至少需要上传 1 帧图片", code=4003, status_code=400)
        if capture_mode not in {"manual", "auto"}:
            raise AppException(message="capture_mode 仅支持 manual 或 auto", code=4223, status_code=422)
        if any(not item_bytes for _, item_bytes in frame_items):
            raise AppException(message="上传的图片为空", code=4003, status_code=400)
<<<<<<< HEAD

        saved_frames = self._save_frame_items(frame_items)
        valid_frames: list[tuple[Path, str, Dict[str, Any]]] = []
        frame_errors: list[str] = []
        minimum_valid_frames = 3 if len(saved_frames) >= 3 else 1

        try:
            for frame_path, frame_relpath in saved_frames:
                try:
                    probe_result = face_engine.extract_single_face_embedding(frame_path)
                    valid_frames.append((frame_path, frame_relpath, probe_result))
                except Exception as exc:
                    frame_errors.append(str(exc))

            if len(valid_frames) < minimum_valid_frames:
                raise AppException(
                    message="连续抓拍帧中有效单人脸数量不足，请正视镜头并缓慢眨眼或轻微转头后重试",
=======
        saved_frames = self._save_frame_items(frame_items)
        minimum_valid_frames = 4 if len(saved_frames) >= 4 else 1

        try:
            valid_frames, frame_errors = self._collect_valid_frames(saved_frames)
            if len(valid_frames) < minimum_valid_frames:
                raise AppException(
                    message="连续采集中有效单人脸帧数量不足，请正视镜头后重试",
>>>>>>> 98bf8e49 (update)
                    code=4225,
                    status_code=422,
                    data={
                        "uploaded_frame_count": len(saved_frames),
                        "valid_frame_count": len(valid_frames),
                        "frame_errors": frame_errors,
                    },
                )

<<<<<<< HEAD
            probe_embedding = self._average_embeddings(
                [frame_result["embedding"] for _, _, frame_result in valid_frames]
            )
            liveness = liveness_engine.evaluate_sequence(
                [frame_path for frame_path, _, _ in valid_frames],
                [frame_result["bbox"] for _, _, frame_result in valid_frames],
            )
        except Exception:
            for frame_path, _ in saved_frames:
                if frame_path.exists():
                    frame_path.unlink(missing_ok=True)
            raise

        middle_index = len(valid_frames) // 2
        primary_frame_path, primary_relpath, primary_probe_result = valid_frames[middle_index]
        emotion_result = emotion_engine.analyze_face(
            primary_frame_path,
            primary_probe_result.get("bbox"),
        )
        base_record = {
            "image_path": primary_relpath,
            "capture_mode": capture_mode,
            "threshold": FACE_MATCH_THRESHOLD,
            "liveness_result": liveness["result"],
            "liveness_score": liveness["score"],
            "liveness_mode": liveness["mode"],
            "frame_count": len(saved_frames),
            "valid_frame_count": len(valid_frames),
            "emotion": emotion_result["emotion"],
            "emotion_score": emotion_result["score"],
            "created_at": self.now_str(),
            "operator_role": current_user.get("role"),
            "operator_username": current_user.get("username"),
        }
=======
            liveness = liveness_engine.evaluate_sequence(
                [frame_path for frame_path, _, _ in valid_frames],
                [frame_result["bbox"] for _, _, frame_result in valid_frames],
                [frame_result.get("landmarks") for _, _, frame_result in valid_frames],
                challenge_id=challenge_id,
                purpose="attendance",
                operator_username=current_user.get("username"),
            )
        except Exception:
            self._cleanup_saved_frames(saved_frames)
            raise

        primary_frame_path, primary_relpath, primary_probe_result = self._select_primary_frame(valid_frames)

        if liveness["result"] == "uncertain":
            self._cleanup_saved_frames(saved_frames)
            return self._build_response_payload(
                status="retry",
                matched=False,
                record_id=None,
                student=None,
                image_path=None,
                capture_mode=capture_mode,
                match_score=0.0,
                bbox=None,
                det_score=None,
                frame_count=len(saved_frames),
                valid_frame_count=len(valid_frames),
                emotion_result=None,
                liveness=liveness,
                threshold=FACE_MATCH_THRESHOLD,
            )
>>>>>>> 98bf8e49 (update)

        if liveness["result"] != "real":
            record = attendance_repo.create(
                {
<<<<<<< HEAD
                    **base_record,
=======
                    "image_path": primary_relpath,
                    "capture_mode": capture_mode,
                    "threshold": FACE_MATCH_THRESHOLD,
                    "liveness_result": liveness["result"],
                    "liveness_score": liveness["score"],
                    "liveness_confidence": liveness["confidence"],
                    "liveness_mode": liveness["verification_mode"],
                    "verification_mode": liveness["verification_mode"],
                    "challenge_result": liveness["challenge_result"],
                    "challenge_action": liveness["challenge_action"],
                    "challenge_action_label": liveness["challenge_action_label"],
                    "challenge_prompt": liveness["challenge_prompt"],
                    "challenge_score": liveness["challenge_score"],
                    "challenge_confidence": liveness.get("challenge_confidence", liveness.get("confidence")),
                    "challenge_threshold": liveness["challenge_threshold"],
                    "challenge_reason": liveness["challenge_reason"],
                    "challenge_details": liveness.get("challenge_details"),
                    "spoof_result": liveness.get("spoof_result"),
                    "spoof_score": liveness.get("spoof_score"),
                    "spoof_confidence": liveness.get("spoof_confidence"),
                    "spoof_attack_type": liveness.get("spoof_attack_type"),
                    "spoof_model_name": liveness.get("spoof_model_name"),
                    "spoof_reason": liveness.get("spoof_reason"),
                    "spoof_real_threshold": liveness.get("spoof_real_threshold"),
                    "spoof_fake_threshold": liveness.get("spoof_fake_threshold"),
                    "frame_count": len(saved_frames),
                    "valid_frame_count": len(valid_frames),
                    "accepted_frame_count": liveness.get("accepted_frame_count"),
                    "rejected_frame_count": liveness.get("rejected_frame_count"),
                    "quality_insufficient": liveness.get("quality_insufficient", False),
                    "frame_debug": liveness.get("frame_debug", []),
>>>>>>> 98bf8e49 (update)
                    "student_id": None,
                    "student_no": None,
                    "student_name": None,
                    "class_name": None,
                    "match_score": 0.0,
                    "status": "rejected",
<<<<<<< HEAD
                    "note": "活体检测未通过，已拒绝本次考勤",
                }
            )
            emotion_service.record_attendance_emotion(
                attendance_record_id=record["id"],
                student_id=None,
                student_no=None,
                student_name=None,
                class_name=None,
                emotion=emotion_result["emotion"],
                emotion_score=emotion_result["score"],
                emotion_mode=emotion_result["mode"],
                image_path=primary_relpath,
                created_at=record["created_at"],
                operator_username=current_user.get("username"),
            )
            return {
                "matched": False,
                "student_id": None,
                "student_no": None,
                "student_name": None,
                "class_name": None,
                "image_path": primary_relpath,
                "capture_mode": capture_mode,
                "match_score": 0.0,
                "threshold": FACE_MATCH_THRESHOLD,
                "status": "rejected",
                "record_id": record["id"],
                "bbox": primary_probe_result["bbox"],
                "det_score": primary_probe_result["det_score"],
                "liveness_result": liveness["result"],
                "liveness_score": liveness["score"],
                "liveness_threshold": liveness["threshold"],
                "liveness_mode": liveness["mode"],
                "frame_count": len(saved_frames),
                "valid_frame_count": len(valid_frames),
                "emotion": emotion_result["emotion"],
                "emotion_score": emotion_result["score"],
            }

        candidates = self.load_active_students_with_features()
        if not candidates:
=======
                    "emotion": None,
                    "emotion_score": None,
                    "created_at": self.now_str(),
                    "operator_role": current_user.get("role"),
                    "operator_username": current_user.get("username"),
                    "challenge_required": False,
                    "challenge_used": liveness.get("challenge_used", False),
                    "attack_suspected": liveness["result"] == "fake",
                    "challenge_id": liveness.get("challenge_id"),
                    "final_decision": "block",
                    "note": liveness.get("reason"),
                }
            )
            return self._build_response_payload(
                status="rejected",
                matched=False,
                record_id=record["id"],
                student=None,
                image_path=primary_relpath,
                capture_mode=capture_mode,
                match_score=0.0,
                bbox=primary_probe_result["bbox"],
                det_score=primary_probe_result["det_score"],
                frame_count=len(saved_frames),
                valid_frame_count=len(valid_frames),
                emotion_result=None,
                liveness=liveness,
                threshold=FACE_MATCH_THRESHOLD,
            )

        emotion_result = self._analyze_emotion_safe(
            primary_frame_path,
            primary_probe_result,
        )
        reference_frames = list(valid_frames)
        probe_embedding = self._average_embeddings(
            [frame_result["embedding"] for _, _, frame_result in reference_frames]
        )

        base_record = {
            "image_path": primary_relpath,
            "capture_mode": capture_mode,
            "threshold": FACE_MATCH_THRESHOLD,
            "liveness_result": liveness["result"],
            "liveness_score": liveness["score"],
            "liveness_confidence": liveness["confidence"],
            "liveness_mode": liveness["verification_mode"],
            "verification_mode": liveness["verification_mode"],
            "challenge_result": liveness["challenge_result"],
            "challenge_action": liveness["challenge_action"],
            "challenge_action_label": liveness["challenge_action_label"],
            "challenge_prompt": liveness["challenge_prompt"],
            "challenge_score": liveness["challenge_score"],
            "challenge_confidence": liveness.get("challenge_confidence", liveness.get("confidence")),
            "challenge_threshold": liveness["challenge_threshold"],
            "challenge_reason": liveness["challenge_reason"],
            "challenge_details": liveness.get("challenge_details"),
            "spoof_result": liveness.get("spoof_result"),
            "spoof_score": liveness.get("spoof_score"),
            "spoof_confidence": liveness.get("spoof_confidence"),
            "spoof_attack_type": liveness.get("spoof_attack_type"),
            "spoof_model_name": liveness.get("spoof_model_name"),
            "spoof_reason": liveness.get("spoof_reason"),
            "spoof_real_threshold": liveness.get("spoof_real_threshold"),
            "spoof_fake_threshold": liveness.get("spoof_fake_threshold"),
            "frame_count": len(saved_frames),
            "valid_frame_count": len(valid_frames),
            "accepted_frame_count": liveness.get("accepted_frame_count"),
            "rejected_frame_count": liveness.get("rejected_frame_count"),
            "quality_insufficient": liveness.get("quality_insufficient", False),
            "frame_debug": liveness.get("frame_debug", []),
            "emotion": None if emotion_result is None else emotion_result["emotion"],
            "emotion_score": None if emotion_result is None else emotion_result["score"],
            "emotion_mode": None if emotion_result is None else emotion_result.get("mode"),
            "created_at": self.now_str(),
            "operator_role": current_user.get("role"),
            "operator_username": current_user.get("username"),
            "challenge_required": False,
            "challenge_used": liveness.get("challenge_used", False),
            "attack_suspected": False,
            "challenge_id": liveness.get("challenge_id"),
            "final_decision": "allow",
            "note": liveness.get("reason"),
        }

        candidates = self.load_active_students_with_features()
        if not candidates:
            self._cleanup_saved_frames(saved_frames)
>>>>>>> 98bf8e49 (update)
            raise AppException(
                message="当前没有可用的人脸特征库，请先为学生上传并提取人脸特征",
                code=4004,
                status_code=400,
            )

        best_student = None
        best_score = -1.0
        for student, feature_path in candidates:
            try:
                gallery_embedding = face_engine.load_embedding(feature_path)
                score = face_engine.cosine_similarity(probe_embedding, gallery_embedding)
            except Exception:
                continue

            if score > best_score:
                best_score = score
                best_student = student

        best_score = round(float(max(best_score, 0.0)), 6)

        if best_student is not None and best_score >= FACE_MATCH_THRESHOLD:
            record = attendance_repo.create(
                {
                    **base_record,
                    "student_id": best_student["id"],
                    "student_no": best_student.get("student_no"),
                    "student_name": best_student.get("name"),
                    "class_name": best_student.get("class_name"),
                    "match_score": best_score,
                    "status": "present",
<<<<<<< HEAD
                    "note": "人脸识别成功",
                }
            )
            emotion_service.record_attendance_emotion(
                attendance_record_id=record["id"],
                student_id=best_student["id"],
                student_no=best_student.get("student_no"),
                student_name=best_student.get("name"),
                class_name=best_student.get("class_name"),
                emotion=emotion_result["emotion"],
                emotion_score=emotion_result["score"],
                emotion_mode=emotion_result["mode"],
                image_path=primary_relpath,
                created_at=record["created_at"],
                operator_username=current_user.get("username"),
            )
            return {
                "matched": True,
                "student_id": best_student["id"],
                "student_no": best_student.get("student_no"),
                "student_name": best_student.get("name"),
                "class_name": best_student.get("class_name"),
                "image_path": primary_relpath,
                "capture_mode": capture_mode,
                "match_score": best_score,
                "threshold": FACE_MATCH_THRESHOLD,
                "status": "present",
                "record_id": record["id"],
                "bbox": primary_probe_result["bbox"],
                "det_score": primary_probe_result["det_score"],
                "liveness_result": liveness["result"],
                "liveness_score": liveness["score"],
                "liveness_threshold": liveness["threshold"],
                "liveness_mode": liveness["mode"],
                "frame_count": len(saved_frames),
                "valid_frame_count": len(valid_frames),
                "emotion": emotion_result["emotion"],
                "emotion_score": emotion_result["score"],
            }
=======
                    "note": self._build_note(liveness, matched=True),
                }
            )
            if emotion_result is not None:
                emotion_service.record_attendance_emotion(
                    attendance_record_id=record["id"],
                    student_id=best_student["id"],
                    student_no=best_student.get("student_no"),
                    student_name=best_student.get("name"),
                    class_name=best_student.get("class_name"),
                    emotion=emotion_result["emotion"],
                    emotion_score=emotion_result["score"],
                    emotion_mode=emotion_result["mode"],
                    image_path=primary_relpath,
                    created_at=record["created_at"],
                    operator_username=current_user.get("username"),
                )
            return self._build_response_payload(
                status="present",
                matched=True,
                record_id=record["id"],
                student=best_student,
                image_path=primary_relpath,
                capture_mode=capture_mode,
                match_score=best_score,
                bbox=primary_probe_result["bbox"],
                det_score=primary_probe_result["det_score"],
                frame_count=len(saved_frames),
                valid_frame_count=len(valid_frames),
                emotion_result=emotion_result,
                liveness=liveness,
                threshold=FACE_MATCH_THRESHOLD,
            )
>>>>>>> 98bf8e49 (update)

        record = attendance_repo.create(
            {
                **base_record,
                "student_id": None,
                "student_no": None,
                "student_name": None,
                "class_name": None,
                "match_score": best_score,
                "status": "unknown",
<<<<<<< HEAD
                "note": "未匹配到已知学生",
            }
        )
        emotion_service.record_attendance_emotion(
            attendance_record_id=record["id"],
            student_id=None,
            student_no=None,
            student_name=None,
            class_name=None,
            emotion=emotion_result["emotion"],
            emotion_score=emotion_result["score"],
            emotion_mode=emotion_result["mode"],
            image_path=primary_relpath,
            created_at=record["created_at"],
            operator_username=current_user.get("username"),
        )
        return {
            "matched": False,
            "student_id": None,
            "student_no": None,
            "student_name": None,
            "class_name": None,
            "image_path": primary_relpath,
            "capture_mode": capture_mode,
            "match_score": best_score,
            "threshold": FACE_MATCH_THRESHOLD,
            "status": "unknown",
            "record_id": record["id"],
            "bbox": primary_probe_result["bbox"],
            "det_score": primary_probe_result["det_score"],
            "liveness_result": liveness["result"],
            "liveness_score": liveness["score"],
            "liveness_threshold": liveness["threshold"],
            "liveness_mode": liveness["mode"],
            "frame_count": len(saved_frames),
            "valid_frame_count": len(valid_frames),
            "emotion": emotion_result["emotion"],
            "emotion_score": emotion_result["score"],
        }
=======
                "note": self._build_note(liveness, matched=False),
            }
        )
        if emotion_result is not None:
            emotion_service.record_attendance_emotion(
                attendance_record_id=record["id"],
                student_id=None,
                student_no=None,
                student_name=None,
                class_name=None,
                emotion=emotion_result["emotion"],
                emotion_score=emotion_result["score"],
                emotion_mode=emotion_result["mode"],
                image_path=primary_relpath,
                created_at=record["created_at"],
                operator_username=current_user.get("username"),
            )
        return self._build_response_payload(
            status="unknown",
            matched=False,
            record_id=record["id"],
            student=None,
            image_path=primary_relpath,
            capture_mode=capture_mode,
            match_score=best_score,
            bbox=primary_probe_result["bbox"],
            det_score=primary_probe_result["det_score"],
            frame_count=len(saved_frames),
            valid_frame_count=len(valid_frames),
            emotion_result=emotion_result,
            liveness=liveness,
            threshold=FACE_MATCH_THRESHOLD,
        )
>>>>>>> 98bf8e49 (update)


attendance_service = AttendanceService()
