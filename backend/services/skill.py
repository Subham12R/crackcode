from typing import Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models.skill import SkillScore
from repositories.problem import ProblemRepository
from repositories.skill import SkillRepository
from repositories.submission import SubmissionRepository
from schemas.analytics import SkillScoreResponse


class SkillService:
    """Service layer for skill scoring and analysis."""

    def __init__(
        self,
        skill_repo: SkillRepository,
        submission_repo: SubmissionRepository,
        problem_repo: ProblemRepository,
    ):
        self.skill_repo = skill_repo
        self.submission_repo = submission_repo
        self.problem_repo = problem_repo

    async def compute_skill_profile(
        self, db: AsyncSession, user_id: str
    ) -> Dict[str, SkillScoreResponse]:
        """Compute or update skill profile for a user."""
        # Get all submissions for user
        submissions = await self.submission_repo.get_by_user(db, user_id)

        # Calculate topic scores
        topic_stats = {}
        for submission in submissions:
            problem = await self.problem_repo.get_by_id(
                db, str(submission.problem_id)
            )
            if not problem:
                continue

            for topic in problem.topics:
                if topic not in topic_stats:
                    topic_stats[topic] = {
                        "total": 0,
                        "accepted": 0,
                        "first_try": 0,
                    }

                topic_stats[topic]["total"] += 1
                if submission.verdict == "accepted":
                    topic_stats[topic]["accepted"] += 1
                if submission.is_first_try:
                    topic_stats[topic]["first_try"] += 1

        # Convert to skill scores
        skills = {}
        for topic, stats in topic_stats.items():
            accuracy = (
                stats["accepted"] / stats["total"]
                if stats["total"] > 0
                else 0.0
            )
            # Score based on accuracy and volume
            volume_factor = min(stats["total"] / 10.0, 1.0)
            score = accuracy * volume_factor
            confidence = volume_factor

            skill_response = SkillScoreResponse(
                topic=topic,
                score=round(score, 2),
                confidence=round(confidence, 2),
                problems_solved=stats["accepted"],
                accuracy_rate=round(accuracy * 100, 2),
            )
            skills[topic] = skill_response

            # Update or create in database
            existing = await self.skill_repo.get_by_user_and_topic(
                db, user_id, topic
            )
            if existing:
                await self.skill_repo.update(
                    db,
                    db_obj=existing,
                    obj_in={
                        "score": score,
                        "confidence": confidence,
                        "problems_solved": stats["accepted"],
                        "accuracy_rate": accuracy * 100,
                    },
                )
            else:
                await self.skill_repo.create(
                    db,
                    obj_in={
                        "user_id": user_id,
                        "topic": topic,
                        "score": score,
                        "confidence": confidence,
                        "problems_solved": stats["accepted"],
                        "accuracy_rate": accuracy * 100,
                    },
                )

        return skills

    async def get_weak_skills(
        self, db: AsyncSession, user_id: str, threshold: float = 0.5
    ) -> List[SkillScore]:
        """Get user's weak skills below threshold."""
        return await self.skill_repo.get_weak_skills(
            db, user_id, threshold
        )

    async def get_skill_graph(
        self, db: AsyncSession, user_id: str
    ) -> Dict[str, SkillScoreResponse]:
        """Get user's skill graph data."""
        # Ensure profile is computed
        await self.compute_skill_profile(db, user_id)

        # Get from database
        skills = await self.skill_repo.get_by_user(db, user_id)
        return {
            skill.topic: SkillScoreResponse(
                topic=skill.topic,
                subtopic=skill.subtopic,
                score=float(skill.score),
                confidence=float(skill.confidence),
                problems_solved=skill.problems_solved,
                accuracy_rate=float(skill.accuracy_rate),
            )
            for skill in skills
        }