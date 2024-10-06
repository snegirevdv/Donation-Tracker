from fastapi import APIRouter

from app.api.endpoints import charity_project, donation

router = APIRouter()

router.include_router(
    charity_project.router,
    prefix='/charity_project',
    tags=['Projects'],
)

router.include_router(
    donation.router,
    prefix='/donation',
    tags=['Donations'],
)
