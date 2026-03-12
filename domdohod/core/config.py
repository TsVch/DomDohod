"""Application configuration loader."""

from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True, slots=True)
class Settings:
    telegram_bot_token: str
    max_bot_token: str
    api_host: str = "0.0.0.0"
    api_port: int = 8000


    @property
    def api_base_url(self) -> str:
        return f"http://{self.api_host}:{self.api_port}"


def get_settings() -> Settings:
    """Build settings from environment variables."""

    return Settings(
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        max_bot_token=os.getenv("MAX_BOT_TOKEN", ""),
        api_host=os.getenv("API_HOST", "0.0.0.0"),
        api_port=int(os.getenv("API_PORT", "8000")),
    )
