from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.core import constants


class ProjectCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=constants.MinLength.PROJECT_NAME,
        max_length=constants.MaxLength.PROJECT_NAME,
        description=constants.Field.PROJECT_NAME,
    )
    description: str = Field(
        ...,
        min_length=constants.MinLength.PROJECT_DESCRIPTION,
        description=constants.Field.PROJECT_DESCRIPTION,
    )
    full_amount: PositiveInt = Field(
        ...,
        description=constants.Field.PROJECT_FULL_AMOUNT,
    )


class ProjectUpdate(BaseModel):
    name: str | None = Field(
        None,
        min_length=constants.MinLength.PROJECT_NAME,
        max_length=constants.MaxLength.PROJECT_NAME,
        description=constants.Field.PROJECT_NAME,
    )
    description: str | None = Field(
        None,
        min_length=constants.MinLength.PROJECT_DESCRIPTION,
        description=constants.Field.PROJECT_DESCRIPTION,
    )
    full_amount: PositiveInt | None = Field(
        None,
        description=constants.Field.PROJECT_FULL_AMOUNT,
    )


class ProjectRead(BaseModel):
    id: int
    name: str
    description: str
    full_amount: PositiveInt
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None

    model_config = ConfigDict(from_attributes=True)
