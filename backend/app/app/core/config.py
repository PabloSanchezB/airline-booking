from pydantic import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    APP_ENV: str = 'dev'
    DATABASE_USERNAME: str = 'airadmin'
    DATABASE_PASSWORD: str = '123123'
    DATABASE_HOST: str = 'airline-az-db.postgres.database.azure.com'
    DATABASE_NAME: str = 'airlinedb'
    TEST_DATABASE_NAME: str = 'airlinedb'
    DATABASE_PARAM: str = "sslmode=require"
    SQLALCHEMY_DATABASE_URI: Optional[str] = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 5
    JWT_SECRET: str = "zsjGXAcHUF4LwvrMw5KNLEV3hNkuqum7AnTDyF4J6qZfPAGSfkSXfQb2VPjL9awpywd4SENJKn"
    ALGORITHM: str = "HS512"
    
    class Config:
        case_sensitive: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()