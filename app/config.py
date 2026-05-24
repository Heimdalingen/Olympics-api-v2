"""Application configuration loaded from environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings): 
    # Main database (Postgres running in Docker)
    database_url: str = "postgresql://postgres:postgres@db:5432/olympics"

    # Number of tokens given to new users on registration
    initial_tokens: int = 10

    # Redis chache URL
    redis_url: str = "redis://cache:6379"

    # Internal microservice URLs (Docker service names as hostnames)
    logger_url: str = "http://logger:8000"
    rate_limiter_url: str = "http://rate-limiter:8000"
    token_shop_url: str = "http://token-shop:8000"

    class Config:
        env_file = ".env"

settings = Settings()