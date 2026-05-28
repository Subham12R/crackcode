from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundException, ValidationException
from core.security import get_password_hash, verify_password
from models.user import User
from repositories.user import UserRepository
from schemas.auth import Token
from schemas.user import UserCreate, UserUpdate


class UserService:
    """Service layer for user business logic."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(
        self, db: AsyncSession, user_data: UserCreate
    ) -> User:
        """Create a new user."""
        # Check if email already exists
        existing = await self.user_repo.get_by_email(db, user_data.email)
        if existing:
            raise ValidationException("Email already registered")

        # Check if username exists (if provided)
        if user_data.username:
            existing_username = await self.user_repo.get_by_username(
                db, user_data.username
            )
            if existing_username:
                raise ValidationException("Username already taken")

        # Hash password and create user
        user_dict = user_data.model_dump()
        user_dict["password_hash"] = get_password_hash(
            user_dict.pop("password")
        )

        return await self.user_repo.create(db, obj_in=user_dict)

    async def authenticate(
        self, db: AsyncSession, email: str, password: str
    ) -> Optional[User]:
        """Authenticate a user by email and password."""
        user = await self.user_repo.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    async def get_user(self, db: AsyncSession, user_id: str) -> User:
        """Get user by ID."""
        user = await self.user_repo.get_by_id(db, user_id)
        if not user:
            raise NotFoundException("User", user_id)
        return user

    async def update_user(
        self, db: AsyncSession, user_id: str, user_data: UserUpdate
    ) -> User:
        """Update user data."""
        user = await self.get_user(db, user_id)
        update_data = user_data.model_dump(exclude_unset=True)
        return await self.user_repo.update(db, db_obj=user, obj_in=update_data)

    async def update_streak(
        self, db: AsyncSession, user_id: str, streak: int
    ) -> User:
        """Update user's streak."""
        user = await self.get_user(db, user_id)
        return await self.user_repo.update_streak(db, user_id, streak)

    async def increment_solved(
        self, db: AsyncSession, user_id: str
    ) -> User:
        """Increment user's solved count."""
        user = await self.get_user(db, user_id)
        return await self.user_repo.increment_solved(db, user_id)