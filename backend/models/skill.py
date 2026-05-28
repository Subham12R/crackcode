from typing import Optional

from sqlalchemy import DECIMAL, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class SkillScore(Base):
    """Per-topic ability scores for users."""

    __tablename__ = "skill_scores"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False, index=True
    )
    topic: Mapped[str] = mapped_column(String(100), nullable=False)
    subtopic: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    score: Mapped[float] = mapped_column(DECIMAL(3, 2), default=0.0)
    confidence: Mapped[float] = mapped_column(DECIMAL(3, 2), default=0.0)
    problems_solved: Mapped[int] = mapped_column(Integer, default=0)
    accuracy_rate: Mapped[float] = mapped_column(DECIMAL(5, 2), default=0.0)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="skill_scores")

    # Constraints
    __table_args__ = (
        UniqueConstraint("user_id", "topic", "subtopic", name="uq_user_topic_subtopic"),
    )