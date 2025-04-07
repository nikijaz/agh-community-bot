from typing import Final

from redis import Redis

from src.utils.config import CONFIG

REDIS_STORE: Final = Redis(
    host=CONFIG.REDIS_HOST,
    port=CONFIG.REDIS_PORT,
    decode_responses=True,
)
