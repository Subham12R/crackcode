from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model."""

    def __init__(self):
        super().__init__(User)

    async def get_by_email(
        self, db: AsyncSession, email: str
    ) -> Optional[User]:
        """Get user by email address."""
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(
        self, db: AsyncSession, username: str
    ) -> Optional[User]:
        """Get user by username."""
        result = await db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def update_streak(
        self, db: AsyncSession, user_id: str, streak: int
    ) -> Optional[User]:
        """Update user's current streak."""
        user = await self.get_by_id(db, user_id)
        if user:
            user.current_streak = streak
            await db.flush()
            await db.refresh(user)
        return user

    async def increment_solved(
        self, db: AsyncSession, user_id: str
    ) -> Optional[User]:
        """Increment user's total solved count."""
        user = await self.get_by_id(db, user_id)
        if user:
            user.total_solved += 1
            await db.flush()
            await db.refresh(user)
        return user