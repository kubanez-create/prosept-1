import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append("")

from src.api.routers import all_routers
from src.core.config import settings
from src.core.init_db import create_first_superuser

origins = [
    "http://localhost",
    "http://localhost:8080",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_first_superuser()
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

# if __name__ == "__main__":
#     uvicorn.run(app="main:app", reload=True)
