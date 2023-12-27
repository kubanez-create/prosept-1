from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str
    database_url: str
    secret: str
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    postgres_user: str
    postgres_password: str
    postgres_db: str
    db_host: str
    db_port: str
    test_user: str
    test_password: str
    test_db: str
    debug: bool

    class Config:
        env_file = ".env"


settings = Settings()
