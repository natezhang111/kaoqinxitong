from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class SecurityTestRecordResponse(BaseModel):
    id: int
    test_type: str
    sample_path: str
    frame_count: int = 1
    valid_frame_count: int = 1
    result: str
    score: float
    confidence: float
    threshold: float
    liveness_mode: str
    created_at: str
    remark: Optional[str] = None


class SecurityTestRunResponse(BaseModel):
    record_id: int
    test_type: str
    sample_path: str
    frame_count: int
    valid_frame_count: int
    result: str
    score: float
    confidence: float
    threshold: float
    liveness_mode: str
    temporal: dict = Field(default_factory=dict)
    created_at: str
