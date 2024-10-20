from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core import constants
from app.models.abstract import BaseModel


class Project(BaseModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_amount: Mapped[int] = mapped_column(Integer)
    invested_amount: Mapped[int] = mapped_column(Integer, default=0)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    close_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    name: Mapped[str] = mapped_column(
        String(constants.MaxLength.PROJECT_NAME),
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(String, nullable=False)

    @property
    def available_amount(self) -> int:
        return self.full_amount - self.invested_amount

    @property
    def fully_invested(self) -> bool:
        return self.invested_amount >= self.full_amount
