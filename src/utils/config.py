import os
from dataclasses import dataclass
from typing import Final

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    TELEGRAM_API_ID: int = int(os.environ["TELEGRAM_API_ID"])
    TELEGRAM_API_HASH: str = os.environ["TELEGRAM_API_HASH"]
    TELEGRAM_BOT_TOKEN: str = os.environ["TELEGRAM_BOT_TOKEN"]

    DATABASE_URL: str = (
        os.environ["DATABASE_URL"]
        .replace("sqlite://", "sqlite+aiosqlite://")
        .replace("postgresql://", "postgresql+asyncpg://")
    )
    REDIS_URL: str = os.environ["REDIS_URL"]


CONFIG: Final = Config()
