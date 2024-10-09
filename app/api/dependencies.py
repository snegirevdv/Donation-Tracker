"""Dependencies for API"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import fastapi_users
from app.models import User

current_user = Depends(fastapi_users.current_user(active=True))
current_superuser = Depends(fastapi_users.current_user(active=True, superuser=True))
session = Depends(get_async_session)

CurrentUser = Annotated[User, current_user]
CurrentSuperuser = Annotated[User, current_superuser]
Session = Annotated[AsyncSession, session]
