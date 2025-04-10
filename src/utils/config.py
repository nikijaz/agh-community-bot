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

    DATABASE_URL: str = os.environ["DATABASE_URL"]

    REDIS_HOST: str = os.environ["REDIS_HOST"]
    REDIS_PORT: int = int(os.environ["REDIS_PORT"])

    CAPTCHA_TIMEOUT: int = int(os.environ["CAPTCHA_TIMEOUT"])
    INACTIVITY_TIMEOUT: int = int(os.environ["INACTIVITY_TIMEOUT"])


CONFIG: Final = Config()
