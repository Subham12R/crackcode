from typing import List, Optional

from sqlalchemy import ARRAY, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Recommendation(Base):
    """Generated practice recommendations."""

    __tablename__ = "recommendations"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False, index=True
    )
    recommendation_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # sheet, contest, revision
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    target_topics: Mapped[List[str]] = mapped_column(
        ARRAY(String), default=list, server_default="{}"
    )
    problem_ids: Mapped[List[str]] = mapped_column(
        ARRAY(String), default=list, server_default="{}"
    )
    generated_at: Mapped[str] = mapped_column(String, nullable=True)
    expires_at: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    acceptance_status: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True
    )
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ml_model_version: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="recommendations")