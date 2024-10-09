from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import constants
from app.core.db import get_async_session
from app.core.settings import settings
from app.models import User
from app.schemas.user import UserCreate


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Custom UserManager for User model."""

    async def validate_password(self, password: str, user: UserCreate | User) -> None:
        min_len = constants.MinLength.USER_PASSWORD
        if len(password) < min_len:
            error = constants.Message.PASSWORD_LEN_ERROR.format(min_len)
            raise InvalidPasswordException(reason=error)

        if user.email in password:
            error = constants.Message.PASSWORD_EMAIL_ERROR
            raise InvalidPasswordException(reason=error)


async def get_jwt_strategy() -> JWTStrategy:
    """Provides JWT strategy required for Authentication Backend."""
    return JWTStrategy(
        secret=settings.secret_key,
        lifetime_seconds=constants.JWT_LIFETIME,
    )


async def get_user_db(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> AsyncGenerator:
    """Provides an asynchronous user database dependency."""
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db: Annotated[AsyncGenerator, Depends(get_user_db)],
) -> AsyncGenerator:
    """Provides an asynchronous user manager dependency."""
    yield UserManager(user_db)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=BearerTransport(tokenUrl='auth/login'),
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
