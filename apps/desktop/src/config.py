"""App configuration via environment variables and runtime settings file."""
import json
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(__file__).parent.parent / ".env"
SETTINGS_FILE = Path.home() / ".lisan" / "settings.json"

_DEFAULTS: dict = {
    "hotkey": "alt+space",
    "language": "auto",
    "cleanup_mode": "light",
    "mic_device": None,
}


class Settings(BaseSettings):
    groq_api_key: str = Field(validation_alias="GROQ_API_KEY")
    hotkey: str = "alt+space"
    language: str = "auto"
    cleanup_mode: str = "light"
    log_level: str = "INFO"
    mic_device: int | None = None

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_prefix="LISAN_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Load settings, merging .env (secrets) with settings.json (runtime prefs)."""
    base = Settings()
    runtime = load_runtime_settings()
    return base.model_copy(update=runtime)


def load_runtime_settings() -> dict:
    """Load mutable settings from ~/.lisan/settings.json."""
    if not SETTINGS_FILE.exists():
        return {}
    try:
        return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_runtime_settings(updates: dict) -> None:
    """Persist mutable settings to ~/.lisan/settings.json and bust the cache."""
    SETTINGS_FILE.parent.mkdir(exist_ok=True)
    current = load_runtime_settings()
    current.update({k: v for k, v in updates.items() if k in _DEFAULTS})
    SETTINGS_FILE.write_text(
        json.dumps(current, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    get_settings.cache_clear()
