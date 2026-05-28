from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_analytics_service, get_skill_service
from core.database import get_db
from core.exceptions import HTTPExceptionMapper
from models.user import User
from schemas.analytics import (
    SkillGraphResponse,
    WeaknessReport,
)
from services.analytics import AnalyticsService
from services.auth import get_current_active_user
from services.skill import SkillService

router = APIRouter()


@router.get("/skill-graph")
async def get_skill_graph(
    db: AsyncSession = Depends(get_db),
    skill_service: SkillService = Depends(get_skill_service),
    current_user: User = Depends(get_current_active_user),
):
    """Get user's skill graph."""
    try:
        skills = await skill_service.get_skill_graph(
            db, str(current_user.id)
        )
        return SkillGraphResponse(
            user_id=current_user.id,
            skills=list(skills.values()),
        )
    except Exception as e:
        raise HTTPExceptionMapper.map(e)


@router.get("/weaknesses")
async def get_weaknesses(
    db: AsyncSession = Depends(get_db),
    analytics_service: AnalyticsService = Depends(
        get_analytics_service
    ),
    current_user: User = Depends(get_current_active_user),
):
    """Get weakness report."""
    try:
        report = await analytics_service.generate_weakness_report(
            db, str(current_user.id)
        )
        return report
    except Exception as e:
        raise HTTPExceptionMapper.map(e)


@router.get("/stats")
async def get_stats(
    db: AsyncSession = Depends(get_db),
    analytics_service: AnalyticsService = Depends(
        get_analytics_service
    ),
    current_user: User = Depends(get_current_active_user),
):
    """Get user statistics."""
    try:
        stats = await analytics_service.get_user_stats(
            db, str(current_user.id)
        )
        return stats
    except Exception as e:
        raise HTTPExceptionMapper.map(e)