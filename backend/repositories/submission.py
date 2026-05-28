from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.submission import Submission
from repositories.base import BaseRepository


class SubmissionRepository(BaseRepository[Submission]):
    """Repository for Submission model."""

    def __init__(self):
        super().__init__(Submission)

    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: str,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Submission]:
        """Get submissions for a specific user."""
        result = await db.execute(
            select(Submission)
            .where(Submission.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_user_and_problem(
        self,
        db: AsyncSession,
        user_id: str,
        problem_id: str
    ) -> List[Submission]:
        """Get all submissions for a user on a specific problem."""
        result = await db.execute(
            select(Submission).where(
                Submission.user_id == user_id,
                Submission.problem_id == problem_id
            )
        )
        return result.scalars().all()

    async def get_user_stats(
        self, db: AsyncSession, user_id: str
    ) -> dict:
        """Get submission statistics for a user."""
        submissions = await self.get_by_user(db, user_id)
        total = len(submissions)
        accepted = len([s for s in submissions if s.verdict == "accepted"])
        return {
            "total_submissions": total,
            "accepted_count": accepted,
            "success_rate": accepted / total if total > 0 else 0.0,
        }