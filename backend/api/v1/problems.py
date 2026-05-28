from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_problem_repo
from core.database import get_db
from core.exceptions import HTTPExceptionMapper
from models.user import User
from repositories.problem import ProblemRepository
from schemas.problem import ProblemResponse, ProblemSearchRequest
from services.auth import get_current_active_user

router = APIRouter()


@router.get("", response_model=List[ProblemResponse])
async def list_problems(
    topics: List[str] = Query(default=[]),
    difficulty: str = Query(default=None),
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0),
    db: AsyncSession = Depends(get_db),
    problem_repo: ProblemRepository = Depends(get_problem_repo),
    current_user: User = Depends(get_current_active_user),
):
    """List problems with optional filtering."""
    try:
        if topics:
            problems = await problem_repo.get_by_topics(
                db, topics, skip=offset, limit=limit
            )
        elif difficulty:
            problems = await problem_repo.get_by_difficulty(
                db, difficulty, skip=offset, limit=limit
            )
        else:
            problems = await problem_repo.get_all(
                db, skip=offset, limit=limit
            )
        return problems
    except Exception as e:
        raise HTTPExceptionMapper.map(e)


@router.get("/{problem_id}", response_model=ProblemResponse)
async def get_problem(
    problem_id: UUID,
    db: AsyncSession = Depends(get_db),
    problem_repo: ProblemRepository = Depends(get_problem_repo),
    current_user: User = Depends(get_current_active_user),
):
    """Get problem by ID."""
    try:
        problem = await problem_repo.get_by_id(db, str(problem_id))
        if not problem:
            from core.exceptions import NotFoundException

            raise NotFoundException("Problem", str(problem_id))
        return problem
    except Exception as e:
        raise HTTPExceptionMapper.map(e)


@router.get("/{problem_id}/similar", response_model=List[ProblemResponse])
async def get_similar_problems(
    problem_id: UUID,
    limit: int = Query(default=5, le=20),
    db: AsyncSession = Depends(get_db),
    problem_repo: ProblemRepository = Depends(get_problem_repo),
    current_user: User = Depends(get_current_active_user),
):
    """Get similar problems using embeddings."""
    try:
        problem = await problem_repo.get_by_id(db, str(problem_id))
        if not problem:
            from core.exceptions import NotFoundException

            raise NotFoundException("Problem", str(problem_id))

        if not problem.embedding_vector:
            return []

        similar = await problem_repo.search_similar(
            db, problem.embedding_vector, limit=limit
        )
        return similar
    except Exception as e:
        raise HTTPExceptionMapper.map(e)