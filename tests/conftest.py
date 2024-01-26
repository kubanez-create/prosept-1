import asyncio
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
from typing import AsyncGenerator

from fastapi import FastAPI
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.dealers import DealerService

sys.path.append("")

from src.utils.unitofwork import UnitOfWork
from src.db.db import get_async_session
from src.schemas.dealers import Dealer
from src.models import Base
from src.api.routers import all_routers
from src.db.db import engine_test, test_async_session_maker


BASE_DIR = Path(__file__).parent
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = "%d.%m.%Y %H:%M:%S"
metadata = Base.metadata
log_dir = BASE_DIR / 'logs'
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'tests.log'

rotating_handler = RotatingFileHandler(
    log_file, maxBytes=10 ** 6, backupCount=5
)
logging.basicConfig(
    datefmt=DT_FORMAT,
    format=LOG_FORMAT,
    level=logging.INFO,
    handlers=(rotating_handler, logging.StreamHandler())
)

app = FastAPI(title="test app", lifespan=None)
for router in all_routers:
    app.include_router(router, prefix="/api")

metadata.bind = engine_test

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session

@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)

# SETUP

@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as ac:
        yield ac

@pytest.fixture
async def add_dealer():
    logging.info("WE INSIDE FIXTURE")
    uow = UnitOfWork()
    async with uow:
        dealer = Dealer(name="Akson")
        dealer_db = await uow.dealers.add_one(dealer.model_dump())
        await uow.commit()
        return dealer_db.id
