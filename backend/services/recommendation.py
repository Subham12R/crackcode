from typing import Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models.problem import Problem
from models.recommendation import Recommendation
from repositories.problem import ProblemRepository
from repositories.recommendation import RecommendationRepository
from repositories.skill import SkillRepository
from schemas.recommendation import (
    RecommendationCreate,
    RecommendationResponse,
)
from services.skill import SkillService


class RecommendationService:
    """Service layer for generating recommendations."""

    def __init__(
        self,
        recommendation_repo: RecommendationRepository,
        problem_repo: ProblemRepository,
        skill_repo: SkillRepository,
    ):
        self.recommendation_repo = recommendation_repo
        self.problem_repo = problem_repo
        self.skill_repo = skill_repo

    async def generate_daily_sheet(
        self, db: AsyncSession, user_id: str
    ) -> Recommendation:
        """Generate daily practice sheet for user."""
        # Get weak skills
        weak_skills = await self.skill_repo.get_weak_skills(db, user_id)

        # Get target topics
        target_topics = []
        if weak_skills:
            target_topics = [skill.topic for skill in weak_skills[:3]]

        # If no weak skills, get random topics
        if not target_topics:
            target_topics = ["arrays", "strings", "hash-table"]

        # Find problems for those topics
        problems = await self.problem_repo.get_by_topics(
            db, target_topics, limit=5
        )

        # Create recommendation
        problem_ids = [str(p.id) for p in problems]
        rec_data = {
            "user_id": user_id,
            "recommendation_type": "sheet",
            "title": f"Daily Practice - {', '.join(target_topics[:2])}",
            "target_topics": target_topics,
            "problem_ids": problem_ids,
        }

        return await self.recommendation_repo.create(db, obj_in=rec_data)

    async def get_similar_problems(
        self, db: AsyncSession, problem_id: str, limit: int = 5
    ) -> List[Problem]:
        """Get semantically similar problems."""
        problem = await self.problem_repo.get_by_id(db, problem_id)
        if not problem or not problem.embedding_vector:
            return []

        return await self.problem_repo.search_similar(
            db, problem.embedding_vector, limit=limit
        )

    async def get_user_recommendations(
        self,
        db: AsyncSession,
        user_id: str,
        rec_type: Optional[str] = None,
    ) -> List[Recommendation]:
        """Get recommendations for user."""
        if rec_type:
            return await self.recommendation_repo.get_by_type(
                db, user_id, rec_type
            )
        return await self.recommendation_repo.get_by_user(db, user_id)

    async def provide_feedback(
        self,
        db: AsyncSession,
        recommendation_id: str,
        feedback: str,
        status: str,
    ) -> Recommendation:
        """Provide feedback on a recommendation."""
        rec = await self.recommendation_repo.get_by_id(db, recommendation_id)
        if not rec:
            from core.exceptions import NotFoundException

            raise NotFoundException("Recommendation", recommendation_id)

        return await self.recommendation_repo.update(
            db,
            db_obj=rec,
            obj_in={
                "feedback": feedback,
                "acceptance_status": status,
            },
        )