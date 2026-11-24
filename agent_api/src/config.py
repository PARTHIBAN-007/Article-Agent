from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, Field

class Settings(BaseSettings):
    """Application settings."""
    OLLAMA_BASE_URL: str = Field(..., env="OLLAMA_BASE_URL")
    OLLAMA_MODEL_NAME: str = Field(..., env="OLLAMA_MODEL_NAME")

    OPENROUTER_BASE_URL: str = Field(..., env="OPENROUTER_BASE_URL")
    OPENROUTER_API_KEY: str = Field(..., env="OPENROUTER_API_KEY")
    OPENROUTER_MODEL_NAME: str = Field(..., env="OPENROUTER_MODEL_NAME")

    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")

from functools import lru_cache

@lru_cache()
def get_settings() -> Settings:
    """Get application settings."""
    return Settings()

