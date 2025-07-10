import pathlib

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    DEBUG: bool
    SECRET_KEY: str
    DATABASE_URL: PostgresDsn

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
