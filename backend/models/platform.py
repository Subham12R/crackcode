from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Platform(Base):
    """Supported coding platforms."""

    __tablename__ = "platforms"

    name_slug: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    base_url: Mapped[str] = mapped_column(String(255), nullable=True)
    auth_type: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relationships
    accounts: Mapped[list["PlatformAccount"]] = relationship(
        "PlatformAccount", back_populates="platform"
    )
    problems: Mapped[list["Problem"]] = relationship(
        "Problem", back_populates="platform"
    )


class PlatformAccount(Base):
    """User's linked platform accounts."""

    __tablename__ = "platform_accounts"

    user_id: Mapped[str] = mapped_column(
        String(36), nullable=False, index=True
    )
    platform_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    access_token: Mapped[str] = mapped_column(Text, nullable=True)
    refresh_token: Mapped[str] = mapped_column(Text, nullable=True)
    last_synced_at: Mapped[str] = mapped_column(
        String, nullable=True
    )
    sync_status: Mapped[str] = mapped_column(
        String(20), default="idle"
    )
    metadata: Mapped[dict] = mapped_column(
        JSONB, default=dict, server_default="{}"
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="platform_accounts")
    platform: Mapped["Platform"] = relationship("Platform", back_populates="accounts")