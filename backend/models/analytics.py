from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class AnalyticsEvent(Base):
    """Append-only analytics events log."""

    __tablename__ = "analytics_events"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False, index=True
    )
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    event_data: Mapped[dict] = mapped_column(
        JSONB, default=dict, server_default="{}"
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="analytics_events")