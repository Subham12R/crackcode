from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from repositories.problem import ProblemRepository
from repositories.recommendation import RecommendationRepository
from repositories.skill import SkillRepository
from repositories.submission import SubmissionRepository
from repositories.user import UserRepository
from services.analytics import AnalyticsService
from services.auth import AuthService
from services.recommendation import RecommendationService
from services.skill import SkillService
from services.user import UserService


# Repository dependencies
def get_user_repo() -> UserRepository:
    return UserRepository()


def get_problem_repo() -> ProblemRepository:
    return ProblemRepository()


def get_submission_repo() -> SubmissionRepository:
    return SubmissionRepository()


def get_skill_repo() -> SkillRepository:
    return SkillRepository()


def get_recommendation_repo() -> RecommendationRepository:
    return RecommendationRepository()


# Service dependencies
def get_user_service(
    user_repo: UserRepository = Depends(get_user_repo),
) -> UserService:
    return UserService(user_repo)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repo),
) -> AuthService:
    return AuthService(user_repo)


def get_skill_service(
    skill_repo: SkillRepository = Depends(get_skill_repo),
    submission_repo: SubmissionRepository = Depends(get_submission_repo),
    problem_repo: ProblemRepository = Depends(get_problem_repo),
) -> SkillService:
    return SkillService(skill_repo, submission_repo, problem_repo)


def get_recommendation_service(
    recommendation_repo: RecommendationRepository = Depends(
        get_recommendation_repo
    ),
    problem_repo: ProblemRepository = Depends(get_problem_repo),
    skill_repo: SkillRepository = Depends(get_skill_repo),
) -> RecommendationService:
    return RecommendationService(
        recommendation_repo, problem_repo, skill_repo
    )


def get_analytics_service(
    skill_repo: SkillRepository = Depends(get_skill_repo),
    submission_repo: SubmissionRepository = Depends(get_submission_repo),
) -> AnalyticsService:
    return AnalyticsService(skill_repo, submission_repo)