import os
from dataclasses import dataclass
from typing import Final

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class AppConfig:
    """Application configuration class."""

    TELEGRAM_API_ID: int = int(os.environ["TELEGRAM_API_ID"])
    TELEGRAM_API_HASH: str = os.environ["TELEGRAM_API_HASH"]
    TELEGRAM_BOT_TOKEN: str = os.environ["TELEGRAM_BOT_TOKEN"]

    DATABASE_USER: str = os.environ["POSTGRES_USER"]
    DATABASE_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_DB: str = os.environ["POSTGRES_DB"]

    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL",
        f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@127.0.0.1:6543/{os.environ['POSTGRES_DB']}",
    ).replace("postgresql://", "postgresql+asyncpg://")


APP_CONFIG: Final = AppConfig()
