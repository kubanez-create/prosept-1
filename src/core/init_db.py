import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from .config import settings
from src.db.db import get_async_session
from .users import get_user_db, get_user_manager
from src.schemas.users import UserSchemaAdd

# Превращаем асинхронные генераторы в асинхронные менеджеры контекста.
get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


# Корутина, создающая юзера с переданным email и паролем.
# Возможно создание суперюзера при передаче аргумента is_superuser=True.
async def create_user(
        email: EmailStr,
        password: str,
        is_superuser: bool = False,
        
):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserSchemaAdd(
                            email=email,
                            password=password,
                            is_superuser=is_superuser
                        )
                    )
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    if (settings.first_superuser_email is not None 
            and settings.first_superuser_password is not None):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )
