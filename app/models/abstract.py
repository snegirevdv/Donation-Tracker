from sqlalchemy.orm import declared_attr

from app.core.db import Base


class BaseModel(Base):
    """Basic abstract model for project."""

    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
