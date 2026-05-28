from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class ProblemBase(BaseModel):
    platform_id: int
    platform_slug: str
    title: str
    url: Optional[HttpUrl] = None
    difficulty: str
    topics: List[str] = []
    subtopics: List[str] = []


class ProblemCreate(ProblemBase):
    acceptance_rate: Optional[float] = None
    runtime_percentile: Optional[float] = None
    metadata: dict = {}


class ProblemResponse(ProblemBase):
    id: UUID
    acceptance_rate: Optional[float] = None
    runtime_percentile: Optional[float] = None
    extra_data: dict

    class Config:
        from_attributes = True


class ProblemSearchRequest(BaseModel):
    topics: Optional[List[str]] = None
    difficulty: Optional[str] = None
    limit: int = 20
    offset: int = 0