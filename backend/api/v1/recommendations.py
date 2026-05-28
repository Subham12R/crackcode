from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_recommendation_service
from core.database import get_db
from core.exceptions import HTTPExceptionMapper
from models.user import User
from schemas.recommendation import (
    RecommendationFeedback,
    RecommendationResponse,
)
from services.auth import get_current_active_user
from services.recommendation import RecommendationService

router = APIRouter()


@router.get("", response_model=List[RecommendationResponse])
async def list_recommendations(
    rec_type: str = None,
    db: AsyncSession = Depends(get_db),
    rec_service: RecommendationService = Depends(
        get_recommendation_service
    ),
    current_user: User = Depends(get_current_active_user),
):
    """List user's recommendations."""
    try:
        recommendations = await rec_service.get_user_recommendations(
            db, str(current_user.id), rec_type
        )
        return recommendations
    except Exception as e:
        raise HTTPExceptionMapper.map(e)


@router.post("/daily", response_model=RecommendationResponse)
async def generate_daily_sheet(
    db: AsyncSession = Depends(get_db),
    rec_service: RecommendationService = Depends(
        get_recommendation_service
    ),
    current_user: User = Depends(get_current_active_user),
):
    """Generate daily practice sheet."""
    try:
        recommendation = await rec_service.generate_daily_sheet(
            db, str(current_user.id)
        )
        return recommendation
    except Exception as e:
        raise HTTPExceptionMapper.map(e)


@router.post("/{recommendation_id}/feedback", response_model=RecommendationResponse)
async def provide_feedback(
    recommendation_id: UUID,
    feedback: RecommendationFeedback,
    db: AsyncSession = Depends(get_db),
    rec_service: RecommendationService = Depends(
        get_recommendation_service
    ),
    current_user: User = Depends(get_current_active_user),
):
    """Provide feedback on a recommendation."""
    try:
        recommendation = await rec_service.provide_feedback(
            db,
            str(recommendation_id),
            feedback.feedback,
            feedback.acceptance_status,
        )
        return recommendation
    except Exception as e:
        raise HTTPExceptionMapper.map(e)