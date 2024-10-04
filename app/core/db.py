from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import settings

engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine)


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as async_session:
        yield async_session
