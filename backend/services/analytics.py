from typing import Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.skill import SkillRepository
from repositories.submission import SubmissionRepository
from schemas.analytics import WeaknessReport


class AnalyticsService:
    """Service layer for analytics and insights."""

    def __init__(
        self,
        skill_repo: SkillRepository,
        submission_repo: SubmissionRepository,
    ):
        self.skill_repo = skill_repo
        self.submission_repo = submission_repo

    async def get_user_stats(
        self, db: AsyncSession, user_id: str
    ) -> Dict:
        """Get comprehensive user statistics."""
        submission_stats = await self.submission_repo.get_user_stats(
            db, user_id
        )
        skills = await self.skill_repo.get_by_user(db, user_id)

        return {
            "submissions": submission_stats,
            "skills_count": len(skills),
            "average_skill_score": (
                sum(float(s.score) for s in skills) / len(skills)
                if skills
                else 0.0
            ),
        }

    async def generate_weakness_report(
        self, db: AsyncSession, user_id: str
    ) -> WeaknessReport:
        """Generate weakness report for user."""
        weak_skills = await self.skill_repo.get_weak_skills(
            db, user_id, threshold=0.5
        )

        weak_topics = [
            {
                "topic": skill.topic,
                "score": float(skill.score),
                "accuracy": float(skill.accuracy_rate),
            }
            for skill in weak_skills
        ]

        # Generate recommendation text
        if weak_topics:
            top_weak = weak_topics[0]
            recommendation = (
                f"Focus on {top_weak['topic']} - your score is "
                f"{top_weak['score']:.0%}. Practice more problems "
                f"in this area to improve."
            )
        else:
            recommendation = (
                "Great job! No major weaknesses detected. "
                "Continue practicing to maintain your skills."
            )

        return WeaknessReport(
            user_id=user_id,
            weak_topics=weak_topics,
            recommendation=recommendation,
            suggested_problems=len(weak_topics) * 3,
        )