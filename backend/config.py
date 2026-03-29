from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    embedding_model: str = "text-embedding-3-small"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
