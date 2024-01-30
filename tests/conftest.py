import asyncio
from datetime import date
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
from typing import AsyncGenerator

from fastapi import FastAPI
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.append("")

from src.utils.unitofwork import UnitOfWork
from src.db.db import get_async_session
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

@pytest.fixture(scope="session")
async def add_dealer_akson():
    uow = UnitOfWork()
    async with uow:
        if dealer_obj := await uow.dealers.find_one(name="Akson"):
            return dealer_obj.id
        else:
            dealer = dict(name="Akson")
            dealer_db = await uow.dealers.add_one(dealer)        
        await uow.commit()
        return dealer_db.id

@pytest.fixture(scope="session")
async def add_dealer_bafus():
    uow = UnitOfWork()
    async with uow:
        if dealer_obj := await uow.dealers.find_one(name="Bafus"):
            return dealer_obj.id
        else:
            dealer = dict(name="Bafus")
            dealer_db = await uow.dealers.add_one(dealer)
        await uow.commit()
        return dealer_db.id

@pytest.fixture
async def add_product():
    uow = UnitOfWork()
    async with uow:
        product = dict(
            id=245,
            article="008-1",
            name_1c=(
                "Антисептик невымываемый для ответственных конструкций "
                "PROSEPT ULTRA, концентрат, 1 л."
            )
        )
        product_db = await uow.products.add_one(product)
        await uow.commit()
        return product_db.id

@pytest.fixture
async def add_dealerprices(add_dealer_akson, add_dealer_bafus):
    uow = UnitOfWork()
    async with uow:
        dp1 = dict(
            product_key="546408",
            price=175.00,
            product_url=(
                "https://akson.ru//p/kontsentrat_prosept_multipower_"
                "dlya_mytya_polov_tsitrus_1l"
            ),
            product_name=(
                "Концентрат Prosept Multipower для мытья полов"
                ", цитрус 1л"
            ),
            date=date.fromisoformat("2023-07-13"),
            dealer_id=add_dealer_akson
        )
        dp2 = dict(
            product_key="546234",
            price=285.00,
            product_url=(
                "https://akson.ru//p/sredstvo_dlya_chistki_lyustr_prosept"
                "_universal_anti_dust_500ml"
            ),
            product_name=(
                "Средство для чистки люстр Prosept Universal"
                " Anti-dust, 500мл"
            ),
            date=date.fromisoformat("2023-07-14"),
            dealer_id=add_dealer_bafus
        )
        _ = await uow.dealerprices.add_one(dp1)
        _ = await uow.dealerprices.add_one(dp2)
        await uow.commit()
        return