from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from app.core import constants
from app.core.db import Base


class BaseModel(Base):
    """Basic abstract model for project."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class User(SQLAlchemyBaseUserTable[int], BaseModel):
    pass


class BaseDonateModel(BaseModel):
    """Basic abstract model for donate-related entities."""

    __abstract__ = True

    full_amount: Mapped[int] = mapped_column(Integer)
    invested_amount: Mapped[int] = mapped_column(Integer, default=0)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    close_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    @property
    def available_amount(self) -> int:
        return self.full_amount - self.invested_amount

    @property
    def fully_invested(self) -> bool:
        return self.invested_amount >= self.full_amount


class Project(BaseDonateModel):
    name: Mapped[str] = mapped_column(
        String(constants.MaxLength.PROJECT_NAME),
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(String, nullable=False)


class Donation(BaseDonateModel):
    comment: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id', name='fk_user_id'),
        nullable=True,
    )
