from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    target_companies: Optional[List[str]] = None
    study_goal: Optional[str] = None
    preferred_difficulty: Optional[str] = None


class UserResponse(UserBase):
    id: UUID
    current_streak: int
    total_solved: int
    target_companies: List[str]
    study_goal: str
    preferred_difficulty: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserInDB(UserBase):
    id: UUID
    password_hash: str
    current_streak: int
    total_solved: int
    created_at: datetime

    class Config:
        from_attributes = True