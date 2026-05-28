from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded strictly from environment variables.
    
    NO hardcoded defaults for sensitive values. The app fails fast 
    if required environment variables are not set.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    APP_NAME: str = "CrackCode API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Database — REQUIRED, no default (contains credentials)
    DATABASE_URL: str = Field(
        ...,  # Ellipsis means required, no default
        description="PostgreSQL connection string. Example: postgresql+asyncpg://user:pass@host/db"
    )
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Redis — localhost default for local dev, override in production
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_POOL_SIZE: int = 10

    # Celery — localhost default for local dev, override in production
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # JWT — REQUIRED, no default
    JWT_SECRET: str = Field(
        ...,
        description="Secret key for JWT signing. Must be a strong random string."
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Platform APIs — public endpoints, safe defaults
    LEETCODE_GRAPHQL_URL: str = "https://leetcode.com/graphql"
    CODEFORCES_API_BASE: str = "https://codeforces.com/api"
    HACKERRANK_API_BASE: str = "https://www.hackerrank.com"

    # ML — safe defaults
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384

    # CORS — localhost default for dev
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.
    
    Fails immediately if required env vars are missing.
    """
    return Settings()