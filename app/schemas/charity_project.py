from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=5,
        max_length=100,
        description='Название проекта (от 5 до 100 символов)',
    )
    description: str | None = Field(
        default=None,
        min_length=10,
        description='Описание проекта (не менее 10 символов)',
    )
    full_amount: PositiveInt | None = Field(
        default=None,
        description='Требуемая сумма (целое число, больше 0)',
    )

    model_config = ConfigDict(from_attributes=True)


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        description='Название проекта (от 5 до 100 символов)',
    )
    description: str = Field(
        ...,
        description='Описание проекта (не менее 10 символов)',
    )
    full_amount: PositiveInt = Field(
        ...,
        description='Требуемая сумма (целое число, больше 0)',
    )


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectRead(CharityProjectBase):
    id: int
    invested_amount: PositiveInt = Field(
        default=0,
        description='Собранная сумма',
    )
    fully_invested: bool = Field(
        default=False,
        description='Указывает, собрана ли полная сумма для проекта',
    )
    create_date: datetime = Field(
        ...,
        description='Дата создания проекта',
    )
    close_date: datetime | None = Field(
        default=None,
        description='Дата закрытия проекта',
    )

    model_config = ConfigDict(
        from_attributes=True,
        fields_order=[
            'id',
            'name',
            'description',
            'full_amount',
            'invested_amount',
            'fully_invested',
            'create_date',
            'close_date',
        ],
    )
