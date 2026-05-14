from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.core.config import (
    ALLOWED_IMAGE_SUFFIXES,
    DATETIME_FORMAT,
    FACE_MATCH_THRESHOLD,
    FEATURES_DIR,
    GROUP_PHOTO_UPLOAD_DIR,
    REPORTS_DIR,
)
from app.core.exceptions import AppException
from app.services.emotion_engine import emotion_engine
from app.services.emotion_service import emotion_service
from app.services.face_engine import face_engine
from app.storage.excel_exporter import export_group_photo_activity
from app.storage.repositories import (
    activities_repo,
    activity_face_results_repo,
    emotion_records_repo,
    students_repo,
)


class GroupPhotoService:
    def now_str(self) -> str:
        return datetime.now().strftime(DATETIME_FORMAT)

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
    def group_photo_relpath(filename: str) -> str:
        return f"uploads/group_photos/{filename}"

    def load_active_students_with_features(self) -> List[tuple[Dict[str, Any], Path]]:
        valid_students: List[tuple[Dict[str, Any], Path]] = []
        for student in students_repo.list_active_students():
            feature_relpath = student.get("face_feature_path")
            if not feature_relpath:
                continue
            feature_path = FEATURES_DIR / Path(str(feature_relpath)).name
            if not feature_path.exists():
                continue
            valid_students.append((student, feature_path))
        return valid_students

    @staticmethod
    def _deduplicate_participants(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        best_by_student: Dict[int, Dict[str, Any]] = {}
        for item in results:
            if item.get("student_id") is None:
                continue
            student_id = int(item["student_id"])
            current_best = best_by_student.get(student_id)
            if current_best is None or item.get("match_score", 0.0) > current_best.get(
                "match_score", 0.0
            ):
                best_by_student[student_id] = item
        return sorted(
            best_by_student.values(),
            key=lambda x: (x.get("class_name") or "", x.get("student_no") or ""),
        )

    def _list_activity_face_rows(self, activity_id: int) -> List[Dict[str, Any]]:
        rows = [
            item
            for item in activity_face_results_repo.list_all()
            if item.get("activity_id") == activity_id
        ]
        rows.sort(key=lambda x: int(x.get("face_index", 0)))
        return rows

    def _refresh_activity_statistics(self, activity_id: int) -> Dict[str, Any]:
        activity = activities_repo.get_by_id(activity_id)
        if activity is None:
            raise AppException(message="活动记录不存在", code=4042, status_code=404)

        rows = self._list_activity_face_rows(activity_id)
        matched_faces = [item for item in rows if item.get("status") == "matched"]
        unknown_faces = [item for item in rows if item.get("status") == "unknown"]
        participants = self._deduplicate_participants(matched_faces)

        updated = activities_repo.update(
            activity_id,
            {
                "face_count": len(rows),
                "matched_count": len(matched_faces),
                "unmatched_count": len(unknown_faces),
                "participant_count": len(participants),
            },
        )
        if updated is None:
            raise AppException(message="更新活动统计失败", code=5004, status_code=500)
        return updated

    def _sync_group_photo_emotion_record(
        self,
        *,
        activity_id: int,
        face_result: Dict[str, Any],
        activity: Dict[str, Any],
    ) -> None:
        target = None
        for item in emotion_records_repo.list_all():
            if (
                item.get("source") == "group_photo"
                and item.get("activity_id") == activity_id
                and item.get("face_index") == face_result.get("face_index")
            ):
                target = item
                break

        payload = {
            "activity_title": activity.get("title"),
            "student_id": face_result.get("student_id"),
            "student_no": face_result.get("student_no"),
            "student_name": face_result.get("student_name"),
            "class_name": face_result.get("class_name"),
            "emotion": face_result.get("emotion"),
            "emotion_score": face_result.get("emotion_score"),
            "emotion_mode": face_result.get("emotion_mode"),
            "bbox": face_result.get("bbox"),
            "image_path": activity.get("image_path"),
            "created_at": face_result.get("created_at"),
        }

<<<<<<< HEAD
=======
        if not face_result.get("emotion") and target is None:
            return

>>>>>>> 98bf8e49 (update)
        if target is None:
            emotion_service.create_record(
                {
                    "source": "group_photo",
                    "source_label": "合照",
                    "attendance_record_id": None,
                    "activity_id": activity_id,
                    "activity_title": activity.get("title"),
                    "student_id": face_result.get("student_id"),
                    "student_no": face_result.get("student_no"),
                    "student_name": face_result.get("student_name"),
                    "class_name": face_result.get("class_name"),
                    "emotion": face_result.get("emotion"),
                    "emotion_score": face_result.get("emotion_score"),
                    "emotion_mode": face_result.get("emotion_mode"),
                    "face_index": face_result.get("face_index"),
                    "bbox": face_result.get("bbox"),
                    "image_path": activity.get("image_path"),
                    "created_at": face_result.get("created_at"),
                    "operator_username": face_result.get("manual_review_by") or activity.get("created_by"),
                }
            )
            return

        emotion_records_repo.update(int(target["id"]), payload)

<<<<<<< HEAD
=======
    @staticmethod
    def _analyze_emotion_safe(
        image_path: Path,
        face: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        try:
            return emotion_engine.analyze_face(
                image_path,
                face.get("bbox"),
                face.get("landmarks"),
            )
        except Exception:
            return None

>>>>>>> 98bf8e49 (update)
    def recognize_group_photo(
        self,
        *,
        file_bytes: bytes,
        filename: Optional[str],
        title: str,
        activity_type: str,
        activity_date: Optional[str],
        current_user: Dict[str, Any],
    ) -> Dict[str, Any]:
        suffix = self.validate_image_filename(filename)
        if not file_bytes:
            raise AppException(message="上传的图片为空", code=4003, status_code=400)
        if not title.strip():
            raise AppException(message="活动名称不能为空", code=4228, status_code=422)

        normalized_activity_type = activity_type.strip() or "class_activity"
        normalized_activity_date = (activity_date or "").strip() or datetime.now().strftime(
            "%Y-%m-%d"
        )

        unique_name = f"group_photo_{uuid4().hex}{suffix}"
        save_path = GROUP_PHOTO_UPLOAD_DIR / unique_name
        save_path.write_bytes(file_bytes)
        image_relpath = self.group_photo_relpath(unique_name)

        try:
            detection = face_engine.extract_multiple_face_embeddings(save_path)
        except Exception:
            if save_path.exists():
                save_path.unlink(missing_ok=True)
            raise

        if detection["count"] == 0:
            if save_path.exists():
                save_path.unlink(missing_ok=True)
            raise AppException(message="合照中未检测到人脸", code=4006, status_code=400)

        candidates = self.load_active_students_with_features()
        if not candidates:
            raise AppException(
                message="当前没有可用的人脸特征库，请先为学生上传并提取人脸特征",
                code=4004,
                status_code=400,
            )

        face_matches: List[Dict[str, Any]] = []
        created_at = self.now_str()

        sorted_faces = sorted(detection["faces"], key=lambda x: (x["bbox"][1], x["bbox"][0]))
        for face_index, face in enumerate(sorted_faces, start=1):
            best_student = None
            best_score = -1.0
<<<<<<< HEAD
            emotion_result = emotion_engine.analyze_face(save_path, face.get("bbox"))
=======
            emotion_result = self._analyze_emotion_safe(save_path, face)
>>>>>>> 98bf8e49 (update)
            for student, feature_path in candidates:
                try:
                    gallery_embedding = face_engine.load_embedding(feature_path)
                    score = face_engine.cosine_similarity(face["embedding"], gallery_embedding)
                except Exception:
                    continue
                if score > best_score:
                    best_score = score
                    best_student = student

            best_score = round(float(max(best_score, 0.0)), 6)
            common_payload = {
                "face_index": face_index,
                "match_score": best_score,
                "det_score": round(float(face["det_score"]), 6),
                "bbox": [round(float(value), 3) for value in face["bbox"]],
<<<<<<< HEAD
                "emotion": emotion_result["emotion"],
                "emotion_score": emotion_result["score"],
                "emotion_mode": emotion_result["mode"],
=======
                "emotion": None if emotion_result is None else emotion_result["emotion"],
                "emotion_score": None if emotion_result is None else emotion_result["score"],
                "emotion_mode": None if emotion_result is None else emotion_result["mode"],
>>>>>>> 98bf8e49 (update)
                "created_at": created_at,
                "manual_review_status": "original",
                "manual_review_action": None,
                "manual_review_note": None,
                "manual_review_by": None,
                "manual_review_at": None,
            }
            if best_student is not None and best_score >= FACE_MATCH_THRESHOLD:
                face_matches.append(
                    {
                        **common_payload,
                        "student_id": best_student["id"],
                        "student_no": best_student.get("student_no"),
                        "student_name": best_student.get("name"),
                        "class_name": best_student.get("class_name"),
                        "status": "matched",
                    }
                )
            else:
                face_matches.append(
                    {
                        **common_payload,
                        "student_id": None,
                        "student_no": None,
                        "student_name": None,
                        "class_name": None,
                        "status": "unknown",
                    }
                )

        matched_faces = [item for item in face_matches if item["status"] == "matched"]
        unknown_faces = [item for item in face_matches if item["status"] == "unknown"]
        participants = self._deduplicate_participants(matched_faces)

        activity = activities_repo.create(
            {
                "title": title.strip(),
                "activity_type": normalized_activity_type,
                "activity_date": normalized_activity_date,
                "image_path": image_relpath,
                "face_count": len(face_matches),
                "matched_count": len(matched_faces),
                "unmatched_count": len(unknown_faces),
                "participant_count": len(participants),
                "created_at": created_at,
                "created_by": current_user.get("username"),
            }
        )

        persisted_face_results = activity_face_results_repo.bulk_create(
            [{**item, "activity_id": activity["id"]} for item in face_matches]
        )
        emotion_service.record_group_photo_emotions(
            activity_id=activity["id"],
            activity_title=activity["title"],
            image_path=activity["image_path"],
            created_at=created_at,
            operator_username=current_user.get("username"),
            face_results=persisted_face_results,
        )

        return {
            "activity_id": activity["id"],
            "title": activity["title"],
            "activity_type": activity["activity_type"],
            "activity_date": activity["activity_date"],
            "image_path": activity["image_path"],
            "face_count": activity["face_count"],
            "matched_count": activity["matched_count"],
            "unmatched_count": activity["unmatched_count"],
            "participant_count": activity["participant_count"],
            "participants": participants,
            "unknown_faces": unknown_faces,
            "all_faces": persisted_face_results,
            "created_at": activity["created_at"],
        }

    def list_activities(
        self,
        *,
        keyword: Optional[str] = None,
        activity_type: Optional[str] = None,
        activity_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        activities = activities_repo.list_all()
        result: List[Dict[str, Any]] = []
        keyword_lower = keyword.strip().lower() if keyword else None

        for item in activities:
            if activity_type and item.get("activity_type") != activity_type:
                continue
            if activity_date and item.get("activity_date") != activity_date:
                continue
            if keyword_lower:
                title = str(item.get("title", "")).lower()
                if keyword_lower not in title:
                    continue
            result.append(item)

        result.sort(key=lambda x: x.get("id", 0), reverse=True)
        return result

    def get_activity(self, activity_id: int) -> Dict[str, Any]:
        activity = activities_repo.get_by_id(activity_id)
        if activity is None:
            raise AppException(message="活动记录不存在", code=4042, status_code=404)

        all_faces = self._list_activity_face_rows(activity_id)
        participants = [item for item in all_faces if item.get("status") == "matched"]
        unknown_faces = [item for item in all_faces if item.get("status") == "unknown"]

        return {
            **activity,
            "participants": self._deduplicate_participants(participants),
            "unknown_faces": unknown_faces,
            "all_faces": all_faces,
        }

    def list_activity_participants(
        self, *, activity_id: int, include_unknown: bool = False
    ) -> List[Dict[str, Any]]:
        result = self._list_activity_face_rows(activity_id)
        if include_unknown:
            return result
        matched = [item for item in result if item.get("status") == "matched"]
        return self._deduplicate_participants(matched)

    def correct_face_result(
        self,
        *,
        activity_id: int,
        face_result_id: int,
        action: str,
        student_id: Optional[int],
        note: Optional[str],
        operator: Dict[str, Any],
    ) -> Dict[str, Any]:
        activity = activities_repo.get_by_id(activity_id)
        if activity is None:
            raise AppException(message="活动记录不存在", code=4042, status_code=404)

        face_result = activity_face_results_repo.get_by_id(face_result_id)
        if face_result is None or face_result.get("activity_id") != activity_id:
            raise AppException(message="人脸结果记录不存在", code=4043, status_code=404)

        if action not in {"assign_student", "mark_unknown"}:
            raise AppException(message="不支持的修正动作", code=4232, status_code=422)

        updates: Dict[str, Any] = {
            "manual_review_status": "reviewed",
            "manual_review_action": action,
            "manual_review_note": note,
            "manual_review_by": operator.get("username"),
            "manual_review_at": self.now_str(),
        }

        if action == "assign_student":
            if student_id is None:
                raise AppException(message="assign_student 必须传入 student_id", code=4233, status_code=422)
            student = students_repo.get_by_id(int(student_id))
            if student is None:
                raise AppException(message="目标学生不存在", code=4041, status_code=404)
            if not student.get("is_active", True):
                raise AppException(message="目标学生已停用，不能分配", code=4234, status_code=422)

            updates.update(
                {
                    "status": "matched",
                    "student_id": int(student["id"]),
                    "student_no": student.get("student_no"),
                    "student_name": student.get("name"),
                    "class_name": student.get("class_name"),
                }
            )
        else:
            updates.update(
                {
                    "status": "unknown",
                    "student_id": None,
                    "student_no": None,
                    "student_name": None,
                    "class_name": None,
                }
            )

        updated_face = activity_face_results_repo.update(face_result_id, updates)
        if updated_face is None:
            raise AppException(message="人工修正保存失败", code=5005, status_code=500)

        updated_activity = self._refresh_activity_statistics(activity_id)
        self._sync_group_photo_emotion_record(
            activity_id=activity_id,
            face_result=updated_face,
            activity=updated_activity,
        )

        return {
            "activity": self.get_activity(activity_id),
            "updated_face": updated_face,
        }

    def export_activity(self, activity_id: int) -> Path:
        activity = activities_repo.get_by_id(activity_id)
        if activity is None:
            raise AppException(message="活动记录不存在", code=4042, status_code=404)

        face_rows = self._list_activity_face_rows(activity_id)
        summary = {
            "activity_id": activity["id"],
            "title": activity.get("title"),
            "activity_type": activity.get("activity_type"),
            "activity_date": activity.get("activity_date"),
            "face_count": activity.get("face_count"),
            "matched_count": activity.get("matched_count"),
            "unmatched_count": activity.get("unmatched_count"),
            "participant_count": activity.get("participant_count"),
            "evaluation_accuracy": activity.get("evaluation_accuracy"),
            "created_at": activity.get("created_at"),
        }
        filename = f"group_photo_activity_{activity_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        output_path = REPORTS_DIR / filename
        return export_group_photo_activity(summary, face_rows, output_path)


group_photo_service = GroupPhotoService()
