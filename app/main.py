from fastapi import FastAPI

from app.api.routers import router
from app.core.settings import settings

app = FastAPI(title=settings.app_title)

app.include_router(router)
