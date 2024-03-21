import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    auth0_client_id: str = os.getenv("AUTH0_CLIENT_ID")
    auth0_client_secret: str = os.getenv("AUTH0_CLIENT_SECRET")
    auth0_domain: str = os.getenv("AUTH0_DOMAIN")
    app_secret_key: str = os.getenv("APP_SECRET_KEY")
    auth0_api_audience: str = os.getenv("AUTH0_API_AUDIENCE", "")
    auth0_issuer: str = os.getenv("AUTH0_ISSUER")
    auth0_algorithms: str = os.getenv("AUTH0_ALGORITHMS")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
