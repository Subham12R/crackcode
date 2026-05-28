from typing import List, Optional

from sqlalchemy import ARRAY, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class User(Base):
    """User model for authentication and preferences."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    total_solved: Mapped[int] = mapped_column(Integer, default=0)
    target_companies: Mapped[List[str]] = mapped_column(
        ARRAY(String), default=list, server_default="{}"
    )
    study_goal: Mapped[str] = mapped_column(
        String(50), default="interview"
    )
    preferred_difficulty: Mapped[str] = mapped_column(
        String(20), default="medium"
    )

    # Relationships
    platform_accounts: Mapped[List["PlatformAccount"]] = relationship(
        "PlatformAccount", back_populates="user", cascade="all, delete-orphan"
    )
    submissions: Mapped[List["Submission"]] = relationship(
        "Submission", back_populates="user", cascade="all, delete-orphan"
    )
    skill_scores: Mapped[List["SkillScore"]] = relationship(
        "SkillScore", back_populates="user", cascade="all, delete-orphan"
    )
    recommendations: Mapped[List["Recommendation"]] = relationship(
        "Recommendation", back_populates="user", cascade="all, delete-orphan"
    )
    analytics_events: Mapped[List["AnalyticsEvent"]] = relationship(
        "AnalyticsEvent", back_populates="user", cascade="all, delete-orphan"
    )