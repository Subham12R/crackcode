from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.skill import SkillScore
from repositories.base import BaseRepository


class SkillRepository(BaseRepository[SkillScore]):
    """Repository for SkillScore model."""

    def __init__(self):
        super().__init__(SkillScore)

    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: str
    ) -> List[SkillScore]:
        """Get all skill scores for a user."""
        result = await db.execute(
            select(SkillScore).where(SkillScore.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_user_and_topic(
        self,
        db: AsyncSession,
        user_id: str,
        topic: str,
        subtopic: Optional[str] = None
    ) -> Optional[SkillScore]:
        """Get specific skill score for a user."""
        query = select(SkillScore).where(
            SkillScore.user_id == user_id,
            SkillScore.topic == topic
        )
        if subtopic:
            query = query.where(SkillScore.subtopic == subtopic)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_weak_skills(
        self,
        db: AsyncSession,
        user_id: str,
        threshold: float = 0.5
    ) -> List[SkillScore]:
        """Get skills below threshold for a user."""
        result = await db.execute(
            select(SkillScore).where(
                SkillScore.user_id == user_id,
                SkillScore.score < threshold
            ).order_by(SkillScore.score.asc())
        )
        return result.scalars().all()