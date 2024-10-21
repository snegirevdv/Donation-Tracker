"""Generic type vars for project services."""

from typing import TypeVar

from pydantic import BaseModel

from app.models import Donation, Project

ModelType = TypeVar('ModelType', bound=Project | Donation)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
