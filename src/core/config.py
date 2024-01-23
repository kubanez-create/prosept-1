import logging
import os
from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore") 
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
    debug: bool = False


settings = Settings()
logging.info(f"SETTINGS:: {settings.model_dump()}")
