from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_auth_service
from core.database import get_db
from schemas.auth import LoginRequest, RefreshRequest, Token
from services.auth import AuthService

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: LoginRequest,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Register a new user and return tokens."""
    from schemas.user import UserCreate
    from services.user import UserService
    from api.deps import get_user_service

    user_service: UserService = Depends(get_user_service)
    user = await user_service.create_user(
        db, UserCreate(email=user_data.email, password=user_data.password)
    )
    return await auth_service.login(db, user_data.email, user_data.password)


@router.post("/login", response_model=Token)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Login and get access token."""
    return await auth_service.login(
        db, credentials.email, credentials.password
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: RefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Refresh access token."""
    return await auth_service.refresh_token(refresh_data.refresh_token)