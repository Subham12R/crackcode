from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Submission(Base):
    """Normalized submission history."""

    __tablename__ = "submissions"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False, index=True
    )
    problem_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("problems.id"), nullable=False, index=True
    )
    platform_submission_id: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    verdict: Mapped[str] = mapped_column(String(50), nullable=False)
    language: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    runtime_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    memory_mb: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    submitted_at: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    attempt_count: Mapped[int] = mapped_column(Integer, default=1)
    is_first_try: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="submissions")
    problem: Mapped["Problem"] = relationship("Problem", back_populates="submissions")