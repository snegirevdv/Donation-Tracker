from typing import Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import BaseDonateModel, CharityProject, Donation
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate
from app.schemas.donation import DonationCreate

ModelType = TypeVar('ModelType', bound=BaseDonateModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class BaseDonateCrud(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: ModelType) -> None:
        self.model: type[ModelType] = model

    async def get_list(self, session: AsyncSession) -> list[ModelType]:
        query = select(self.model)
        result = await session.scalars(query)
        return result.all()

    async def create(
        self, obj_in: CreateSchemaType, session: AsyncSession
    ) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        return db_obj


class ProjectCrud(BaseDonateCrud[CharityProject, CharityProjectCreate]):
    async def get(self, obj_id: int, session: AsyncSession) -> ModelType | None:
        query = select(self.model).where(self.model.id == obj_id)
        return await session.scalar(query)

    async def get_id_by_name(self, name: str, session: AsyncSession) -> int | None:
        query = select(self.model.id).where(self.model.name == name)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def update(
        self,
        db_obj: ModelType,
        obj_in: CharityProjectUpdate,
        session: AsyncSession,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: ModelType, session: AsyncSession) -> None:
        await session.delete(db_obj)
        await session.commit()


class DonationCrud(BaseDonateCrud[Donation, DonationCreate]):
    pass


charity_project_crud = ProjectCrud(model=CharityProject)
donation_crud = DonationCrud(model=Donation)
