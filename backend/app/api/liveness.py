from __future__ import annotations

from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.services.liveness_engine import liveness_engine
from app.utils.response import success_response

router = APIRouter(prefix="/liveness", tags=["liveness"])


class ChallengeRequest(BaseModel):
    purpose: str = Field(
        default="attendance",
        description="challenge purpose: attendance or security_test",
    )


@router.post("/challenge")
async def create_liveness_challenge(
    payload: ChallengeRequest,
    current_user=Depends(get_current_user),
):
    challenge = liveness_engine.issue_challenge(
        purpose=payload.purpose,
        operator_username=current_user.get("username"),
        operator_role=current_user.get("role"),
    )
    return success_response(data=challenge)
