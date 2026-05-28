from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.problem import Problem
from repositories.base import BaseRepository


class ProblemRepository(BaseRepository[Problem]):
    """Repository for Problem model."""

    def __init__(self):
        super().__init__(Problem)

    async def get_by_platform_slug(
        self,
        db: AsyncSession,
        platform_id: int,
        platform_slug: str
    ) -> Optional[Problem]:
        """Get problem by platform-specific slug."""
        result = await db.execute(
            select(Problem).where(
                Problem.platform_id == platform_id,
                Problem.platform_slug == platform_slug
            )
        )
        return result.scalar_one_or_none()

    async def get_by_difficulty(
        self,
        db: AsyncSession,
        difficulty: str,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Problem]:
        """Get problems by difficulty level."""
        result = await db.execute(
            select(Problem)
            .where(Problem.difficulty == difficulty)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_topics(
        self,
        db: AsyncSession,
        topics: List[str],
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Problem]:
        """Get problems matching any of the given topics."""
        result = await db.execute(
            select(Problem)
            .where(Problem.topics.overlap(topics))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def search_similar(
        self,
        db: AsyncSession,
        embedding: list,
        *,
        limit: int = 10
    ) -> List[Problem]:
        """Search for similar problems using vector similarity."""
        result = await db.execute(
            select(Problem)
            .order_by(Problem.embedding_vector.cosine_distance(embedding))
            .limit(limit)
        )
        return result.scalars().all()