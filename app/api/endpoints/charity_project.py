from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectRead,
    CharityProjectUpdate,
)

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post(
    '/',
    response_model=CharityProjectRead,
    response_model_exclude_none=True,
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: SessionDep,
) -> CharityProject:
    return await charity_project_crud.create(charity_project, session)


@router.get(
    '/',
    response_model=list[CharityProjectRead],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(session: SessionDep) -> list[CharityProject]:
    return await charity_project_crud.get_list(session)


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectRead,
    response_model_exclude_none=True,
)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: SessionDep,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    return await charity_project_crud.update(charity_project, obj_in, session)


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectRead,
    response_model_exclude_none=True,
)
async def remove_charity_room(charity_project_id: int, session: SessionDep) -> None:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    return await charity_project_crud.delete(charity_project, session)
