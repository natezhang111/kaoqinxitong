from __future__ import annotations

from pydantic import BaseModel, Field


class DashboardStatsResponse(BaseModel):
    total_activities: int
    total_faces_detected: int
    total_unique_participants: int
    evaluated_activity_count: int
    average_accuracy: float


class ActivityFrequencyItem(BaseModel):
    student_id: int
    student_no: str
    student_name: str
    class_name: str
    activity_count: int


class ActivityAccuracyItem(BaseModel):
    activity_id: int
    title: str
    activity_date: str
    activity_type: str
    actual_student_count: int | None = None
    correct_match_count: int | None = None
    accuracy: float | None = None
    matched_count: int
    participant_count: int


class ReportStatsResponse(BaseModel):
    dashboard: dict = Field(default_factory=dict)
    activity_frequency: list[dict] = Field(default_factory=list)
    activity_accuracy: list[dict] = Field(default_factory=list)
    activity_type_distribution: list[dict] = Field(default_factory=list)
