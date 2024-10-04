from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import DonateGenericModel


class CharityProject(DonateGenericModel):
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    desciption: Mapped[str] = mapped_column(String, nullable=False)
