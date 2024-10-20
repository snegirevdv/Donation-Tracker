from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.abstract import BaseModel


class User(SQLAlchemyBaseUserTable[int], BaseModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
