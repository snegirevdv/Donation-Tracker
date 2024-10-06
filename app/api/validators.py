from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate
from app.services.crud import charity_project_crud


async def check_project_name_duplicate(
    obj_in: CharityProjectCreate | CharityProjectUpdate,
    session: AsyncSession,
) -> None:
    if obj_in.name is None:
        return

    project_id = await charity_project_crud.get_id_by_name(obj_in.name, session)

    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


def check_project_full_amount_higher_than_invested(
    obj_in: CharityProjectUpdate,
    obj_db: CharityProject,
) -> None:
    if obj_in.full_amount is not None and obj_in.full_amount < obj_db.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Нельзя установить значение full_amount меньше уже вложенной суммы.',
        )


def check_project_open(obj_db: CharityProject) -> None:
    if obj_db.fully_invested is True:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!',
        )


def check_project_not_invested(obj_db: CharityProject) -> None:
    if obj_db.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


def check_project_exists(obj_db: CharityProject) -> None:
    if obj_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
