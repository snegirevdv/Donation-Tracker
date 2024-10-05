from fastapi import APIRouter

from app.api.endpoints import charity_project, donation

router = APIRouter()

router.include_router(
    charity_project.router,
    prefix='/charity_projects',
    tags=['Charity Projects'],
)

router.include_router(
    donation.router,
    prefix='/donations',
    tags=['Donations'],
)
