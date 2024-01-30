import logging
from logging.handlers import RotatingFileHandler
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append("")

from src.api.routers import all_routers
from src.core.config import settings
from src.core.init_db import create_first_superuser
from src.core.predictions import scheduler
from tests.conftest import BASE_DIR, LOG_FORMAT, DT_FORMAT

origins = [
    "*",
    "http://localhost",
    "http://localhost:5173",
    "http://192.168.56.1:5173",
    "http://81.31.246.233:5173",
]

def configure_logging():
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'api.log'

    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_first_superuser()
    configure_logging()
    # await scheduler()
    yield


app = FastAPI(title=settings.app_title, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for router in all_routers:
    app.include_router(router, prefix="/api")
