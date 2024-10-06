from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseDonateModel(BaseModel):
    __abstract__ = True

    full_amount: Mapped[int] = mapped_column(Integer)
    invested_amount: Mapped[int] = mapped_column(Integer, default=0)
    fully_invested: Mapped[bool] = mapped_column(Boolean, default=False)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    close_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    @property
    def available_amount(self) -> int:
        return self.full_amount - self.invested_amount


class CharityProject(BaseDonateModel):
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)


class Donation(BaseDonateModel):
    comment: Mapped[str] = mapped_column(String, nullable=True)
