from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class AttendanceRecordResponse(BaseModel):
    id: int
    student_id: Optional[int] = None
    student_no: Optional[str] = None
    student_name: Optional[str] = None
    class_name: Optional[str] = None
    image_path: str
    capture_mode: str = Field(description="manual/auto")
    match_score: float
    threshold: float
    status: str = Field(description="present/unknown/rejected")
    liveness_result: Optional[str] = None
    liveness_score: Optional[float] = None
    liveness_mode: Optional[str] = None
    frame_count: int = 1
    valid_frame_count: int = 1
    emotion: Optional[str] = None
    emotion_score: Optional[float] = None
    created_at: str
    note: Optional[str] = None


class AttendanceRecognizeResponse(BaseModel):
    matched: bool
    student_id: Optional[int] = None
    student_no: Optional[str] = None
    student_name: Optional[str] = None
    class_name: Optional[str] = None
    image_path: str
    capture_mode: str
    match_score: float
    threshold: float
    status: str
    record_id: int
    liveness_result: str
    liveness_score: float
    liveness_threshold: float
    liveness_mode: str
    frame_count: int
    valid_frame_count: int
    emotion: Optional[str] = None
    emotion_score: Optional[float] = None


class AttendanceQueryParams(BaseModel):
    keyword: Optional[str] = None
    class_name: Optional[str] = None
    status: Optional[str] = None
    capture_mode: Optional[str] = None
    liveness_result: Optional[str] = None
    emotion: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
