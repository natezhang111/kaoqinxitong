from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, time
from typing import Any, Dict, List, Optional, Sequence

from app.core.config import DATETIME_FORMAT
from app.core.exceptions import AppException
<<<<<<< HEAD
=======
from app.services.emotion_labels import EMOTION_LABELS_ZH, ordered_emotion_keys
>>>>>>> 98bf8e49 (update)
from app.storage.repositories import emotion_records_repo


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


class EmotionService:
    def now_str(self) -> str:
        return datetime.now().strftime(DATETIME_FORMAT)

    @staticmethod
    def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
        normalized = dict(record)
        normalized.setdefault("source", "attendance")
        normalized.setdefault("source_label", "考勤")
        normalized.setdefault("emotion", "neutral")
        normalized.setdefault("emotion_score", 0.0)
        normalized.setdefault("emotion_mode", "heuristic_face_texture")
        normalized.setdefault("student_id", None)
        normalized.setdefault("student_no", None)
        normalized.setdefault("student_name", None)
        normalized.setdefault("class_name", None)
        normalized.setdefault("activity_id", None)
        normalized.setdefault("activity_title", None)
        normalized.setdefault("attendance_record_id", None)
        normalized.setdefault("face_index", None)
        normalized.setdefault("bbox", None)
        normalized.setdefault("image_path", None)
        return normalized

<<<<<<< HEAD
=======
    def _available_emotions(self, rows: Sequence[Dict[str, Any]]) -> List[str]:
        return ordered_emotion_keys(item.get("emotion") for item in rows if item.get("emotion"))

>>>>>>> 98bf8e49 (update)
    def create_record(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        record = emotion_records_repo.create(payload)
        return self.normalize_record(record)

    def bulk_create_records(self, payloads: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not payloads:
            return []
        records = emotion_records_repo.bulk_create(list(payloads))
        return [self.normalize_record(item) for item in records]

    def record_attendance_emotion(
        self,
        *,
        attendance_record_id: int,
        student_id: Optional[int],
        student_no: Optional[str],
        student_name: Optional[str],
        class_name: Optional[str],
        emotion: str,
        emotion_score: float,
        emotion_mode: str,
        image_path: Optional[str],
        created_at: str,
        operator_username: Optional[str],
    ) -> Dict[str, Any]:
        return self.create_record(
            {
                "source": "attendance",
                "source_label": "考勤",
                "attendance_record_id": attendance_record_id,
                "activity_id": None,
                "activity_title": None,
                "student_id": student_id,
                "student_no": student_no,
                "student_name": student_name,
                "class_name": class_name,
                "emotion": emotion,
                "emotion_score": emotion_score,
                "emotion_mode": emotion_mode,
                "face_index": None,
                "bbox": None,
                "image_path": image_path,
                "created_at": created_at,
                "operator_username": operator_username,
            }
        )

    def record_group_photo_emotions(
        self,
        *,
        activity_id: int,
        activity_title: str,
        image_path: Optional[str],
        created_at: str,
        operator_username: Optional[str],
        face_results: Sequence[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        payloads = []
        for item in face_results:
<<<<<<< HEAD
=======
            if not item.get("emotion"):
                continue
>>>>>>> 98bf8e49 (update)
            payloads.append(
                {
                    "source": "group_photo",
                    "source_label": "合照",
                    "attendance_record_id": None,
                    "activity_id": activity_id,
                    "activity_title": activity_title,
                    "student_id": item.get("student_id"),
                    "student_no": item.get("student_no"),
                    "student_name": item.get("student_name"),
                    "class_name": item.get("class_name"),
                    "emotion": item.get("emotion"),
                    "emotion_score": item.get("emotion_score"),
                    "emotion_mode": item.get("emotion_mode"),
                    "face_index": item.get("face_index"),
                    "bbox": item.get("bbox"),
                    "image_path": image_path,
                    "created_at": created_at,
                    "operator_username": operator_username,
                }
            )
        return self.bulk_create_records(payloads)

    def list_records(
        self,
        *,
        keyword: Optional[str] = None,
        source: Optional[str] = None,
        emotion: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        records = [self.normalize_record(item) for item in emotion_records_repo.list_all()]
        dt_start = _parse_date_start(start_date)
        dt_end = _parse_date_end(end_date)
        keyword_lower = keyword.strip().lower() if keyword else None

        result: List[Dict[str, Any]] = []
        for item in records:
            if source and item.get("source") != source:
                continue
            if emotion and item.get("emotion") != emotion:
                continue

            if keyword_lower:
                haystacks = [
                    str(item.get("student_no", "")).lower(),
                    str(item.get("student_name", "")).lower(),
                    str(item.get("activity_title", "")).lower(),
                ]
                if all(keyword_lower not in haystack for haystack in haystacks):
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

    def dashboard(self) -> Dict[str, Any]:
        records = self.list_records()
        source_counter = Counter(item.get("source") for item in records)
        emotion_counter = Counter(item.get("emotion") for item in records)
        scores = [
            float(item.get("emotion_score", 0.0))
            for item in records
            if item.get("emotion_score") is not None
        ]
        dominant_emotion = emotion_counter.most_common(1)[0][0] if emotion_counter else None

        return {
            "total_records": len(records),
            "attendance_records": source_counter.get("attendance", 0),
            "group_photo_records": source_counter.get("group_photo", 0),
            "average_score": round(sum(scores) / len(scores), 6) if scores else 0.0,
            "dominant_emotion": dominant_emotion,
        }

    def emotion_distribution(self) -> List[Dict[str, Any]]:
<<<<<<< HEAD
        counter = Counter(item.get("emotion") for item in self.list_records())
        return [{"emotion": key, "count": value} for key, value in counter.most_common()]
=======
        rows = self.list_records()
        counter = Counter(item.get("emotion") for item in rows if item.get("emotion"))
        ordered = self._available_emotions(rows)
        output = [
            {
                "emotion": key,
                "label": EMOTION_LABELS_ZH.get(key, key),
                "count": int(counter.get(key, 0)),
            }
            for key in ordered
            if counter.get(key, 0) > 0
        ]
        output.sort(key=lambda item: item["count"], reverse=True)
        return output
>>>>>>> 98bf8e49 (update)

    def source_distribution(self) -> List[Dict[str, Any]]:
        counter = Counter(item.get("source") for item in self.list_records())
        return [{"source": key, "count": value} for key, value in counter.most_common()]

    def student_summary(self) -> List[Dict[str, Any]]:
        grouped: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
        for item in self.list_records():
            student_id = item.get("student_id")
            if student_id is None:
                continue
            grouped[int(student_id)].append(item)

        rows: List[Dict[str, Any]] = []
        for student_id, items in grouped.items():
<<<<<<< HEAD
            emotion_counter = Counter(item.get("emotion") for item in items)
            scores = [float(item.get("emotion_score", 0.0)) for item in items]
            latest = max(items, key=lambda x: x.get("id", 0))
=======
            emotion_counter = Counter(item.get("emotion") for item in items if item.get("emotion"))
            scores = [float(item.get("emotion_score", 0.0)) for item in items if item.get("emotion_score") is not None]
            latest = max(items, key=lambda x: x.get("id", 0))
            dominant_emotion = emotion_counter.most_common(1)[0][0] if emotion_counter else None
>>>>>>> 98bf8e49 (update)
            rows.append(
                {
                    "student_id": student_id,
                    "student_no": latest.get("student_no"),
                    "student_name": latest.get("student_name"),
                    "class_name": latest.get("class_name"),
                    "record_count": len(items),
<<<<<<< HEAD
                    "dominant_emotion": emotion_counter.most_common(1)[0][0],
=======
                    "dominant_emotion": dominant_emotion,
>>>>>>> 98bf8e49 (update)
                    "average_score": round(sum(scores) / len(scores), 6) if scores else 0.0,
                }
            )

        rows.sort(key=lambda x: (-int(x["record_count"]), str(x.get("student_no") or "")))
        return rows

    def daily_trend(self) -> List[Dict[str, Any]]:
<<<<<<< HEAD
        buckets: Dict[str, Counter[str]] = defaultdict(Counter)
        for item in self.list_records():
=======
        rows = self.list_records()
        tracked_emotions = self._available_emotions(rows)
        buckets: Dict[str, Counter[str]] = defaultdict(Counter)
        for item in rows:
>>>>>>> 98bf8e49 (update)
            created_at = item.get("created_at")
            try:
                day = datetime.strptime(created_at, DATETIME_FORMAT).strftime("%Y-%m-%d")
            except Exception:
                continue
<<<<<<< HEAD
            buckets[day][str(item.get("emotion"))] += 1

        rows = []
        for day in sorted(buckets.keys()):
            counter = buckets[day]
            rows.append(
                {
                    "date": day,
                    "happy": counter.get("happy", 0),
                    "neutral": counter.get("neutral", 0),
                    "serious": counter.get("serious", 0),
                    "tired": counter.get("tired", 0),
                    "excited": counter.get("excited", 0),
                    "total": sum(counter.values()),
                }
            )
        return rows

    def report(self) -> Dict[str, Any]:
=======
            emotion = str(item.get("emotion") or "").strip()
            if emotion:
                buckets[day][emotion] += 1

        output = []
        for day in sorted(buckets.keys()):
            counter = buckets[day]
            row = {"date": day, "total": sum(counter.values())}
            for emotion in tracked_emotions:
                row[emotion] = int(counter.get(emotion, 0))
            output.append(row)
        return output

    def report(self) -> Dict[str, Any]:
        rows = self.list_records()
        available_emotions = self._available_emotions(rows)
>>>>>>> 98bf8e49 (update)
        return {
            "dashboard": self.dashboard(),
            "emotion_distribution": self.emotion_distribution(),
            "source_distribution": self.source_distribution(),
            "student_summary": self.student_summary(),
            "daily_trend": self.daily_trend(),
<<<<<<< HEAD
=======
            "available_emotions": available_emotions,
            "emotion_labels": {
                key: EMOTION_LABELS_ZH.get(key, key)
                for key in available_emotions
            },
>>>>>>> 98bf8e49 (update)
        }


emotion_service = EmotionService()
