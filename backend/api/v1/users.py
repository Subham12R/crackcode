from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_user_service
from core.database import get_db
from core.exceptions import HTTPExceptionMapper
from models.user import User
from schemas.user import UserCreate, UserResponse, UserUpdate
from services.auth import get_current_active_user
from services.user import UserService

router = APIRouter()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
):
    """Create a new user."""
    try:
        user = await user_service.create_user(db, user_data)
        return user
    except Exception as e:
        raise HTTPExceptionMapper.map(e)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
):
    """Get current user info."""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service),
):
    """Update current user."""
    try:
        user = await user_service.update_user(
            db, str(current_user.id), user_data
        )
        return user
    except Exception as e:
        raise HTTPExceptionMapper.map(e)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
):
    """Get user by ID."""
    try:
        user = await user_service.get_user(db, str(user_id))
        return user
    except Exception as e:
        raise HTTPExceptionMapper.map(e)