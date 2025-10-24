"""
Application configuration management using environment variables.
"""
import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "Football Analytics API"
    debug: bool = False
    version: str = "1.0.0"
    
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@db:5432/football_analytics"
    )
    
    # Database pool settings
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_pre_ping: bool = True
    
    # CORS
    cors_origins: list[str] = ["*"]
    cors_credentials: bool = True
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]
    
    # API-Football Configuration
    api_football_key: str = os.getenv("API_FOOTBALL_KEY", "")
    api_football_base_url: str = os.getenv(
        "API_FOOTBALL_BASE_URL", 
        "https://v3.football.api-sports.io"
    )
    api_football_rate_limit: int = 10  # requests per minute (free tier)
    api_football_timeout: int = 30  # seconds
    
    # Caching
    cache_ttl_seconds: int = 300  # 5 minutes default cache
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
