from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from app.core.config import REPORTS_DIR
from app.storage.excel_exporter import export_statistics_report
from app.storage.repositories import (
    activities_repo,
    activity_face_results_repo,
    evaluation_records_repo,
)


class StatisticsService:
    @staticmethod
    def _deduplicate_faces_by_student(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        best_by_student: Dict[int, Dict[str, Any]] = {}
        for item in results:
            student_id = item.get("student_id")
            if student_id is None:
                continue
            current_best = best_by_student.get(student_id)
            if current_best is None or item.get("match_score", 0.0) > current_best.get(
                "match_score", 0.0
            ):
                best_by_student[int(student_id)] = item
        return list(best_by_student.values())

    def _evaluation_map(self) -> Dict[int, Dict[str, Any]]:
        return {
            int(item["activity_id"]): item
            for item in evaluation_records_repo.list_all()
            if item.get("activity_id") is not None
        }

    def dashboard(self) -> Dict[str, Any]:
        activities = activities_repo.list_all()
        results = activity_face_results_repo.list_all()
        evaluation_map = self._evaluation_map()

        total_faces_detected = sum(int(item.get("face_count", 0)) for item in activities)
        unique_participants = {
            int(item["student_id"])
            for item in results
            if item.get("status") == "matched" and item.get("student_id") is not None
        }

        accuracies = [
            float(item.get("accuracy", 0.0))
            for item in evaluation_map.values()
            if item.get("accuracy") is not None
        ]

        average_accuracy = round(sum(accuracies) / len(accuracies), 6) if accuracies else 0.0

        return {
            "total_activities": len(activities),
            "total_faces_detected": total_faces_detected,
            "total_unique_participants": len(unique_participants),
            "evaluated_activity_count": len(accuracies),
            "average_accuracy": average_accuracy,
        }

    def activity_frequency(self) -> List[Dict[str, Any]]:
        results = activity_face_results_repo.list_all()
        matched_results = [item for item in results if item.get("status") == "matched"]

        grouped: Dict[int, List[Dict[str, Any]]] = {}
        for item in matched_results:
            activity_id = int(item.get("activity_id", 0))
            grouped.setdefault(activity_id, []).append(item)

        participant_counter: Counter[int] = Counter()
        participant_meta: Dict[int, Dict[str, Any]] = {}

        for activity_results in grouped.values():
            deduped = self._deduplicate_faces_by_student(activity_results)
            for item in deduped:
                student_id = int(item["student_id"])
                participant_counter[student_id] += 1
                participant_meta[student_id] = {
                    "student_id": student_id,
                    "student_no": item.get("student_no"),
                    "student_name": item.get("student_name"),
                    "class_name": item.get("class_name"),
                }

        output = []
        for student_id, count in participant_counter.most_common():
            output.append(
                {
                    **participant_meta[student_id],
                    "activity_count": count,
                }
            )
        return output

    def activity_accuracy(self) -> List[Dict[str, Any]]:
        activities = activities_repo.list_all()
        evaluation_map = self._evaluation_map()
        output: List[Dict[str, Any]] = []

        for activity in sorted(activities, key=lambda x: x.get("id", 0), reverse=True):
            evaluation = evaluation_map.get(int(activity["id"]))
            output.append(
                {
                    "activity_id": activity["id"],
                    "title": activity.get("title"),
                    "activity_date": activity.get("activity_date"),
                    "activity_type": activity.get("activity_type"),
                    "actual_student_count": evaluation.get("actual_student_count")
                    if evaluation
                    else None,
                    "correct_match_count": evaluation.get("correct_match_count")
                    if evaluation
                    else None,
                    "accuracy": evaluation.get("accuracy") if evaluation else None,
                    "matched_count": int(activity.get("matched_count", 0)),
                    "participant_count": int(activity.get("participant_count", 0)),
                }
            )
        return output

    def activity_type_distribution(self) -> List[Dict[str, Any]]:
        activities = activities_repo.list_all()
        counter = Counter(str(item.get("activity_type", "unknown")) for item in activities)
        return [{"activity_type": key, "count": value} for key, value in counter.items()]

    def report(self) -> Dict[str, Any]:
        return {
            "dashboard": self.dashboard(),
            "activity_frequency": self.activity_frequency(),
            "activity_accuracy": self.activity_accuracy(),
            "activity_type_distribution": self.activity_type_distribution(),
        }

    def export_report(self) -> Path:
        filename = f"statistics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        output_path = REPORTS_DIR / filename
        return export_statistics_report(self.report(), output_path)


statistics_service = StatisticsService()
