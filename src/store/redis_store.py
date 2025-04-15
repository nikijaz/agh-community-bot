from typing import Final

from redis.asyncio import Redis

from src.utils.config import CONFIG

REDIS_STORE: Final = Redis.from_url(
    CONFIG.REDIS_URL,
    decode_responses=True,
)
