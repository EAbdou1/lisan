"""App configuration via environment variables."""
from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve .env relative to this file (src/../.env → apps/desktop/.env)
_ENV_FILE = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    groq_api_key: str = Field(validation_alias="GROQ_API_KEY")
    hotkey: str = "alt+space"
    language: str = "auto"
    cleanup_mode: str = "light"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_prefix="LISAN_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()