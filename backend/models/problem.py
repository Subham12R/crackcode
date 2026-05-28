from typing import List, Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import ARRAY, DECIMAL, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.config import get_settings
from models.base import Base

settings = get_settings()


class Problem(Base):
    """Unified problem catalog across platforms."""

    __tablename__ = "problems"

    platform_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("platforms.id"), nullable=False, index=True
    )
    platform_slug: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=True)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False)
    topics: Mapped[List[str]] = mapped_column(
        ARRAY(String), default=list, server_default="{}"
    )
    subtopics: Mapped[List[str]] = mapped_column(
        ARRAY(String), default=list, server_default="{}"
    )
    acceptance_rate: Mapped[Optional[float]] = mapped_column(
        DECIMAL(5, 2), nullable=True
    )
    runtime_percentile: Mapped[Optional[float]] = mapped_column(
        DECIMAL(5, 2), nullable=True
    )
    embedding_vector: Mapped[Optional[list]] = mapped_column(
        Vector(settings.EMBEDDING_DIMENSION), nullable=True
    )
    extra_data: Mapped[dict] = mapped_column(
        JSONB, default=dict, server_default="{}"
    )

    # Relationships
    platform: Mapped["Platform"] = relationship("Platform", back_populates="problems")
    submissions: Mapped[List["Submission"]] = relationship(
        "Submission", back_populates="problem"
    )