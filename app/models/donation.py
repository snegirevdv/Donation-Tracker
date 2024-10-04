from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import DonateGenericModel


class Donation(DonateGenericModel):
    comment: Mapped[str] = mapped_column(String)
