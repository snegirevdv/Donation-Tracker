"""CRUD operations for SQL Alchemy models."""

from typing import Generic

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, Project, User
from app.schemas.donation import DonationCreate
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.types import CreateSchemaType, ModelType


class BaseDonateCrud(Generic[ModelType, CreateSchemaType]):
    """Provides list reading and creation operation for donate-related entities."""

    def __init__(self, model: type[ModelType]) -> None:
        self.model: type[ModelType] = model

    async def get_list(self, session: AsyncSession) -> list[ModelType]:
        query = select(self.model)
        result = await session.scalars(query)
        return result.all()

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
        user: User | None = None,
    ) -> ModelType:
        obj_in_data = obj_in.model_dump()

        if user is not None:
            obj_in_data['user_id'] = user.id

        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()

        return db_obj


class ProjectCrud(BaseDonateCrud[Project, ProjectCreate]):
    """Additional CRUD methods for Project model."""

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
        obj_in: ProjectUpdate,
        session: AsyncSession,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        if db_obj.full_amount <= db_obj.invested_amount:
            db_obj.close_date = func.now()

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: ModelType, session: AsyncSession) -> None:
        await session.delete(db_obj)
        await session.commit()


class DonationCrud(BaseDonateCrud[Donation, DonationCreate]):
    """Additional CRUD methods for Donation model."""

    async def get_by_user(self, session: AsyncSession, user: User) -> list[Donation]:
        query = select(self.model).where(self.model.user_id == user.id)
        donations = await session.execute(query)
        return donations.scalars().all()


project_crud = ProjectCrud(model=Project)
donation_crud = DonationCrud(model=Donation)
