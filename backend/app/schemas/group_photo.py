from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class GroupPhotoRecognizeResponse(BaseModel):
    activity_id: int
    title: str
    activity_type: str
    activity_date: str
    image_path: str
    face_count: int
    matched_count: int
    unmatched_count: int
    participant_count: int
    participants: list[dict] = Field(default_factory=list)
    unknown_faces: list[dict] = Field(default_factory=list)
    created_at: str


class ActivityResponse(BaseModel):
    id: int
    title: str
    activity_type: str
    activity_date: str
    image_path: str
    face_count: int
    matched_count: int
    unmatched_count: int
    created_at: str


class ActivityFaceResultResponse(BaseModel):
    id: int
    activity_id: int
    student_id: Optional[int] = None
    student_no: Optional[str] = None
    student_name: Optional[str] = None
    class_name: Optional[str] = None
    match_score: float
    det_score: float
    bbox: list[float]
    emotion: Optional[str] = None
    emotion_score: Optional[float] = None
    emotion_mode: Optional[str] = None
    status: str
    created_at: str
