"""App configuration via environment variables."""
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    groq_api_key: str = Field(..., env="GROQ_API_KEY")
    hotkey: str = Field("alt+space", env="LISAN_HOTKEY")
    language: str = Field("auto", env="LISAN_LANGUAGE")
    cleanup_mode: str = Field("light", env="LISAN_CLEANUP_MODE")

    model_config = {"env_file": ".env"}


@lru_cache
def get_settings() -> Settings:
    return Settings()