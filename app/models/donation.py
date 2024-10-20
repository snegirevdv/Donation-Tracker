from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.abstract import BaseModel


class Donation(BaseModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_amount: Mapped[int] = mapped_column(Integer)
    invested_amount: Mapped[int] = mapped_column(Integer, default=0)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    close_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    comment: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id', name='fk_user_id'),
        nullable=True,
    )

    @property
    def available_amount(self) -> int:
        return self.full_amount - self.invested_amount

    @property
    def fully_invested(self) -> bool:
        return self.invested_amount >= self.full_amount
