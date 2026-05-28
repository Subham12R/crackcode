from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SubmissionBase(BaseModel):
    user_id: UUID
    problem_id: UUID
    verdict: str
    language: Optional[str] = None
    runtime_ms: Optional[int] = None
    memory_mb: Optional[int] = None


class SubmissionCreate(SubmissionBase):
    platform_submission_id: Optional[str] = None
    submitted_at: Optional[str] = None
    attempt_count: int = 1
    is_first_try: bool = True


class SubmissionResponse(SubmissionBase):
    id: UUID
    platform_submission_id: Optional[str] = None
    attempt_count: int
    is_first_try: bool
    submitted_at: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True