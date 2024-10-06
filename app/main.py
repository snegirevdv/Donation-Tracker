from fastapi import FastAPI

from app.api.router import router
from app.core.settings import settings

app = FastAPI(title=settings.app_title, description=settings.app_description)

app.include_router(router)
