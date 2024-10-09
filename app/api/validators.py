"""Additional validators for API."""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import constants
from app.models import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services import project_crud


async def check_project_name_duplicate(
    obj_in: ProjectCreate | ProjectUpdate,
    session: AsyncSession,
) -> None:
    if obj_in.name is None:
        return

    project_id = await project_crud.get_id_by_name(obj_in.name, session)

    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=constants.Message.PROJECT_EXISTS,
        )


def check_project_full_amount_higher_than_invested(
    obj_in: ProjectUpdate,
    obj_db: Project,
) -> None:
    if obj_in.full_amount is not None and obj_in.full_amount < obj_db.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=constants.Message.PROJECT_SMALL_FULL_AMOUNT,
        )


def check_project_open(obj_db: Project) -> None:
    if obj_db.fully_invested is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=constants.Message.PROJECT_CLOSED,
        )


def check_project_not_invested(obj_db: Project) -> None:
    if obj_db.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=constants.Message.PROJECT_INVESTED,
        )


def check_project_exists(obj_db: Project) -> None:
    if obj_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
