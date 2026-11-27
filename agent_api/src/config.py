from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./.env", extra="ignore")
    OLLAMA_BASE_URL: str 
    OLLAMA_MODEL_NAME: str 
    OLLAMA_EMBEDDING_MODEL_NAME: str

    user_agent: str = "article-agent/0.1 (welcome@articleagent.com)"
    request_timeout_s: float = 15.0
    max_article_bytes: int = 5_000_000

    OPENROUTER_BASE_URL: str 
    OPENROUTER_API_KEY: str 
    OPENROUTER_MODEL_NAME: str 
    OPENROUTER_EMBEDDING_MODEL_NAME: str 

    POSTGRES_HOST: str 


from functools import lru_cache

@lru_cache()
def get_settings() -> Settings:
    """Get application settings."""
    return Settings()

