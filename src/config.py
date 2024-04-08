import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    SERVICE_HOST: str = os.getenv("SERVICE_HOST")
    SERVICE_PORT: int = os.getenv("SERVICE_PORT")
    AUTH0_CLIENT_ID: str = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET: str = os.getenv("AUTH0_CLIENT_SECRET")
    AUTH0_DOMAIN: str = os.getenv("AUTH0_DOMAIN")
    APP_SECRET_KEY: str = os.getenv("APP_SECRET_KEY")
    AUTH0_API_AUDIENCE: str = os.getenv("AUTH0_API_AUDIENCE", "")
    AUTH0_ISSUER: str = os.getenv("AUTH0_ISSUER")
    AUTH0_ALGORITHMS: str = os.getenv("AUTH0_ALGORITHMS")
    SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
