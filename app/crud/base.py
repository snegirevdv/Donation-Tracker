from typing import Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
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
