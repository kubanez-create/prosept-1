from fastapi import APIRouter

from src.core.users import auth_backend, fastapi_users
from src.schemas.users import UserSchemaAdd, UserSchemaReturn

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
