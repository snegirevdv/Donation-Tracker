from typing import Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, DonateGenericModel, Donation
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate
from app.schemas.donation import DonationCreate, DonationUpdate

ModelType = TypeVar('ModelType', bound=DonateGenericModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseDonateCrud(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType) -> None:
        self.model: type[ModelType] = model

    async def get(self, obj_id: int, session: AsyncSession) -> ModelType | None:
        query = select(self.model).where(self.model.id == obj_id)
        return await session.scalar(query)

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
    ) -> ModelType | None:
        if not hasattr(self.model, attr_name):
            return None

        attr = getattr(self.model, attr_name)
        query = select(self.model).where(attr == attr_value)
        return await session.scalar(query)

    async def get_available_list(self, session: AsyncSession) -> list[ModelType]:
        query = select(self.model).where(self.model.fully_invested is False)
        result = await session.scalars(query)
        return result.all()

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
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
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


class ProjectCrud(
    BaseDonateCrud[CharityProject, CharityProjectCreate, CharityProjectUpdate],
):
    pass


class DonationCrud(BaseDonateCrud[Donation, DonationCreate, DonationUpdate]):
    pass


charity_project_crud = ProjectCrud(model=CharityProject)
donation_crud = DonationCrud(model=Donation)
