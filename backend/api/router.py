from fastapi import APIRouter

from api.v1 import (
    analytics,
    auth,
    problems,
    recommendations,
    submissions,
    users,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(
    problems.router, prefix="/problems", tags=["Problems"]
)
api_router.include_router(
    submissions.router, prefix="/submissions", tags=["Submissions"]
)
api_router.include_router(
    recommendations.router,
    prefix="/recommendations",
    tags=["Recommendations"],
)
api_router.include_router(
    analytics.router, prefix="/analytics", tags=["Analytics"]
)