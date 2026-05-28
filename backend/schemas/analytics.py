from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel


class SkillScoreResponse(BaseModel):
    topic: str
    subtopic: Optional[str] = None
    score: float
    confidence: float
    problems_solved: int
    accuracy_rate: float

    class Config:
        from_attributes = True


class SkillGraphResponse(BaseModel):
    user_id: UUID
    skills: List[SkillScoreResponse]
    updated_at: Optional[str] = None


class WeaknessReport(BaseModel):
    user_id: UUID
    weak_topics: List[Dict[str, float]]
    recommendation: str
    suggested_problems: int