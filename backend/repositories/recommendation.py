from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.recommendation import Recommendation
from repositories.base import BaseRepository


class RecommendationRepository(BaseRepository[Recommendation]):
    """Repository for Recommendation model."""

    def __init__(self):
        super().__init__(Recommendation)

    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: str,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Recommendation]:
        """Get recommendations for a specific user."""
        result = await db.execute(
            select(Recommendation)
            .where(Recommendation.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_active_by_user(
        self,
        db: AsyncSession,
        user_id: str
    ) -> List[Recommendation]:
        """Get active (non-expired) recommendations for a user."""
        result = await db.execute(
            select(Recommendation).where(
                Recommendation.user_id == user_id,
                Recommendation.acceptance_status.is_(None)
            )
        )
        return result.scalars().all()

    async def get_by_type(
        self,
        db: AsyncSession,
        user_id: str,
        recommendation_type: str
    ) -> List[Recommendation]:
        """Get recommendations by type for a user."""
        result = await db.execute(
            select(Recommendation).where(
                Recommendation.user_id == user_id,
                Recommendation.recommendation_type == recommendation_type
            )
        )
        return result.scalars().all()