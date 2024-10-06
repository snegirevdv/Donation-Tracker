from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class CharityProjectCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=5,
        max_length=100,
        description='Название проекта (от 5 до 100 символов)',
    )
    description: str = Field(
        ...,
        min_length=10,
        description='Описание проекта (не менее 10 символов)',
    )
    full_amount: PositiveInt = Field(
        ...,
        description='Требуемая сумма (целое число, больше 0)',
    )

    model_config = ConfigDict(extra='forbid')


class CharityProjectUpdate(BaseModel):
    name: str | None = Field(
        None,
        min_length=5,
        max_length=100,
        description='Название проекта (от 5 до 100 символов)',
    )
    description: str | None = Field(
        None,
        min_length=10,
        description='Описание проекта (не менее 10 символов)',
    )
    full_amount: PositiveInt | None = Field(
        None,
        description='Требуемая сумма (целое число, больше 0)',
    )

    model_config = ConfigDict(extra='forbid')


class CharityProjectRead(BaseModel):
    id: int
    name: str
    description: str
    full_amount: PositiveInt
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None

    model_config = ConfigDict(from_attributes=True)
