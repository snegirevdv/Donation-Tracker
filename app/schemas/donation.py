from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.core import constants


class DonationCreate(BaseModel):
    full_amount: PositiveInt = Field(
        ...,
        description=constants.Field.DONATION_FULL_AMOUNT,
    )
    comment: str | None = Field(
        default=None,
        description=constants.Field.DONATION_COMMENT,
    )

    model_config = ConfigDict(extra='forbid')


class BaseDonationRead(BaseModel):
    id: int
    comment: str | None
    full_amount: int
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class ExtendedDonationRead(BaseDonationRead):
    invested_amount: int
    fully_invested: bool
    close_date: datetime | None
    user_id: int
