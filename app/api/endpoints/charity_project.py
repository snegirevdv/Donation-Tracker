from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_project_exists,
    check_project_full_amount_higher_than_invested,
    check_project_name_duplicate,
    check_project_not_invested,
    check_project_open,
)
from app.core.db import get_async_session
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectRead,
    CharityProjectUpdate,
)
from app.services.crud import charity_project_crud
from app.services.investment import investment_service

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post('/', response_model=CharityProjectRead)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: SessionDep,
) -> CharityProject:
    await check_project_name_duplicate(charity_project, session)
    project = await charity_project_crud.create(charity_project, session)
    return await investment_service.invest_donations_to_project(project, session)


@router.get(
    '/',
    response_model=list[CharityProjectRead],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(session: SessionDep) -> list[CharityProject]:
    return await charity_project_crud.get_list(session)


@router.patch('/{charity_project_id}', response_model=CharityProjectRead)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: SessionDep,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)

    check_project_exists(charity_project)
    check_project_open(charity_project)
    check_project_full_amount_higher_than_invested(obj_in, charity_project)
    await check_project_name_duplicate(obj_in, session)

    return await charity_project_crud.update(charity_project, obj_in, session)


@router.delete('/{charity_project_id}', response_model=CharityProjectRead)
async def remove_charity_project(charity_project_id: int, session: SessionDep) -> None:
    charity_project = await charity_project_crud.get(charity_project_id, session)

    check_project_exists(charity_project)
    check_project_not_invested(charity_project)

    await charity_project_crud.delete(charity_project, session)
    return charity_project
