from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_submission_repo
from core.database import get_db
from core.exceptions import HTTPExceptionMapper
from models.user import User
from repositories.submission import SubmissionRepository
from schemas.submission import SubmissionCreate, SubmissionResponse
from services.auth import get_current_active_user

router = APIRouter()


@router.get("", response_model=List[SubmissionResponse])
async def list_submissions(
    db: AsyncSession = Depends(get_db),
    submission_repo: SubmissionRepository = Depends(get_submission_repo),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
):
    """List user's submissions."""
    try:
        submissions = await submission_repo.get_by_user(
            db, str(current_user.id), skip=skip, limit=limit
        )
        return submissions
    except Exception as e:
        raise HTTPExceptionMapper.map(e)


@router.post("", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def create_submission(
    submission_data: SubmissionCreate,
    db: AsyncSession = Depends(get_db),
    submission_repo: SubmissionRepository = Depends(get_submission_repo),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new submission."""
    try:
        submission_data.user_id = current_user.id
        submission = await submission_repo.create(
            db, obj_in=submission_data.model_dump()
        )
        return submission
    except Exception as e:
        raise HTTPExceptionMapper.map(e)


@router.get("/stats")
async def get_submission_stats(
    db: AsyncSession = Depends(get_db),
    submission_repo: SubmissionRepository = Depends(get_submission_repo),
    current_user: User = Depends(get_current_active_user),
):
    """Get submission statistics."""
    try:
        stats = await submission_repo.get_user_stats(
            db, str(current_user.id)
        )
        return stats
    except Exception as e:
        raise HTTPExceptionMapper.map(e)