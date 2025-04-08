import asyncio
import time
from typing import TypedDict, cast

from redis import Redis
from telethon import TelegramClient

from src.store.redis_store import REDIS_STORE


class CaptchaData(TypedDict):
    message_id: int


class CaptchaManager:
    def __init__(self, bot: TelegramClient):
        self.bot = bot
        self.redis: Redis = REDIS_STORE

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.__monitor_captcha_timeout())

    async def __monitor_captcha_timeout(self) -> None:
        while True:
            current_time = time.time()
            expired_keys: list[str] = self.redis.zrangebyscore(
                "captcha_timeouts", 0, current_time
            )

            for key in expired_keys:
                chat_id, user_id = key.split(":")
                captcha_key = f"captcha:{chat_id}:{user_id}"
                data: CaptchaData = cast(CaptchaData, self.redis.hgetall(captcha_key))

                self.loop.create_task(
                    self.__handle_captcha_timeout(int(chat_id), int(user_id), data)
                )
                self.redis.delete(captcha_key)

                self.redis.zrem("captcha_timeouts", key)

            await asyncio.sleep(5)

    async def __handle_captcha_timeout(
        self, chat_id: int, user_id: int, captcha_data: CaptchaData
    ) -> None:
        message_id = captcha_data["message_id"]

        await self.bot.delete_messages(chat_id, message_id)
        await self.bot.kick_participant(chat_id, user_id)

    def get_captcha_data(self, chat_id: int, user_id: int) -> CaptchaData | None:
        captcha_key = f"captcha:{chat_id}:{user_id}"
        data = self.redis.hgetall(captcha_key)

        if not data:
            return None
        return cast(CaptchaData, data)

    def add_captcha_timeout(
        self, chat_id: int, user_id: int, expires_at: float, captcha_data: CaptchaData
    ) -> None:
        captcha_key = f"captcha:{chat_id}:{user_id}"

        self.redis.hset(
            captcha_key,
            mapping=cast(dict, captcha_data),
        )

        self.redis.zadd(
            "captcha_timeouts",
            {f"{chat_id}:{user_id}": expires_at},
        )

    def remove_captcha_timeout(self, chat_id: int, user_id: int) -> None:
        captcha_key = f"captcha:{chat_id}:{user_id}"
        self.redis.delete(captcha_key)
        self.redis.zrem("captcha_timeouts", f"{chat_id}:{user_id}")
