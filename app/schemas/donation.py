from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt = Field(
        ..., description='Сумма пожертвования (обязательное поле)'
    )
    comment: str | None = Field(default=None, description='Комментарий к пожертвованию')

    model_config = ConfigDict(extra='forbid')


class DonationRead(BaseModel):
    id: int
    comment: str | None
    full_amount: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None
    user_id: int

    model_config = ConfigDict(from_attributes=True)
