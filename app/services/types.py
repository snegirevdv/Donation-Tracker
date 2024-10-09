"""Generic type vars for project services."""

from typing import TypeVar

from pydantic import BaseModel

from app.models import BaseDonateModel

ModelType = TypeVar('ModelType', bound=BaseDonateModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
