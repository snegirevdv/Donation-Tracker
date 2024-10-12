from fastapi import APIRouter, status

from app.api import dependencies, validators
from app.models import Project
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services import investment_service, project_crud

router = APIRouter()


@router.post(
    '/',
    response_model=ProjectRead,
    dependencies=(dependencies.current_superuser,),
    status_code=status.HTTP_201_CREATED,
)
async def create_new_project(
    project: ProjectCreate,
    session: dependencies.Session,
) -> Project:
    await validators.check_project_name_duplicate(project, session)
    project_obj: Project = await project_crud.create(project, session)
    return await investment_service.invest_donations_to_project(project_obj, session)


@router.get(
    '/',
    response_model=list[ProjectRead],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: dependencies.Session,
) -> list[Project]:
    return await project_crud.get_list(session)


@router.patch(
    '/{project_id}',
    response_model=ProjectRead,
    dependencies=[dependencies.current_superuser],
)
async def update_project(
    project_id: int,
    obj_in: ProjectUpdate,
    session: dependencies.Session,
) -> Project:
    project = await project_crud.get(project_id, session)

    validators.check_project_exists(project)
    validators.check_project_open(project)
    validators.check_project_full_amount_higher_than_invested(obj_in, project)

    await validators.check_project_name_duplicate(obj_in, session)
    return await project_crud.update(project, obj_in, session)


@router.delete(
    '/{project_id}',
    dependencies=[dependencies.current_superuser],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_project(project_id: int, session: dependencies.Session) -> None:
    project = await project_crud.get(project_id, session)

    validators.check_project_exists(project)
    validators.check_project_not_invested(project)

    await project_crud.delete(project, session)
