from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.core.config import settings

engine = create_async_engine(settings.database_url, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session

# DATABASE

DATABASE_URL_TEST = (
    f"postgresql+asyncpg://{settings.test_user}:{settings.test_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.test_db}"
)

engine_test = create_async_engine(
    DATABASE_URL_TEST,
    poolclass=NullPool,
    echo=True,
    future=True
)
test_async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False)