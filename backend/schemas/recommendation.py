from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class RecommendationBase(BaseModel):
    user_id: UUID
    recommendation_type: str
    title: Optional[str] = None
    target_topics: List[str] = []
    problem_ids: List[str] = []


class RecommendationCreate(RecommendationBase):
    expires_at: Optional[str] = None
    ml_model_version: Optional[str] = None


class RecommendationResponse(RecommendationBase):
    id: UUID
    generated_at: Optional[str] = None
    expires_at: Optional[str] = None
    acceptance_status: Optional[str] = None
    feedback: Optional[str] = None
    ml_model_version: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True


class RecommendationFeedback(BaseModel):
    acceptance_status: str
    feedback: Optional[str] = None