from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DonationBase(BaseModel):
    full_amount: int | None = Field(
        default=None,
        gt=0,
        description='Сумма пожертвования (должна быть больше 0)',
    )
    comment: str | None = Field(
        default=None,
        description='Комментарий к пожертвованию',
    )

    model_config = ConfigDict(from_attributes=True)


class DonationCreate(DonationBase):
    full_amount: int = Field(
        ...,
        gt=0,
        description='Сумма пожертвования (обязательное поле)',
    )


class DonationRead(DonationBase):
    id: int
    invested_amount: int = Field(
        default=0,
        description='Сумма, распределенная по проектам',
    )
    fully_invested: bool = Field(
        default=False,
        description='Полностью ли пожертвование распределено',
    )
    create_date: datetime = Field(
        ...,
        description='Дата создания пожертвования',
    )
    close_date: datetime | None = Field(
        default=None,
        description='Дата закрытия пожертвования',
    )

    model_config = ConfigDict(
        from_attributes=True,
        fields_order=[
            'id',
            'comment',
            'full_amount',
            'invested_amount',
            'fully_invested',
            'create_date',
            'close_date',
        ],
    )


class DonationUpdate(DonationBase):
    pass
