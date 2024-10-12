"""Main API router."""

from fastapi import APIRouter

from app.api.endpoints import auth, donation, project, user

router = APIRouter()

router.include_router(
    project.router,
    prefix='/projects',
    tags=['Projects'],
)

router.include_router(
    donation.router,
    prefix='/donations',
    tags=['Donations'],
)

router.include_router(
    auth.router,
    prefix='/auth',
    tags=['Authentication'],
)

router.include_router(
    user.router,
    prefix='/users',
    tags=['Users'],
)
