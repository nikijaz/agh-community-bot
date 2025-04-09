import asyncio
import time
from typing import Required, TypedDict

from telethon import TelegramClient

from src.store.redis_store import REDIS_STORE


class CaptchaData(TypedDict):
    message_id: Required[int]
    button_id: Required[str]


class CaptchaManager:
    def __init__(self, bot: TelegramClient):
        self.bot = bot
        self.redis = REDIS_STORE

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.__monitor_captcha_timeout())

    async def __monitor_captcha_timeout(self) -> None:
        while True:
            current_time = time.time()
            expired_keys: list[str] = await self.redis.zrangebyscore(
                "captcha_timeouts", 0, current_time
            )

            for key in expired_keys:
                chat_id, user_id = key.split(":")
                captcha_key = f"captcha:{chat_id}:{user_id}"
                data = await self.redis.hgetall(captcha_key)
                captcha_data = CaptchaData(
                    message_id=int(data["message_id"]), button_id=data["button_id"]
                )

                self.loop.create_task(
                    self.__handle_captcha_timeout(
                        int(chat_id), int(user_id), captcha_data
                    )
                )
                await self.redis.delete(captcha_key)

                await self.redis.zrem("captcha_timeouts", key)

            await asyncio.sleep(5)

    async def __handle_captcha_timeout(
        self, chat_id: int, user_id: int, captcha_data: CaptchaData
    ) -> None:
        message_id = captcha_data["message_id"]

        await self.bot.delete_messages(chat_id, message_id)
        await self.bot.kick_participant(chat_id, user_id)

    async def get_captcha_data(self, chat_id: int, user_id: int) -> CaptchaData | None:
        captcha_key = f"captcha:{chat_id}:{user_id}"
        data = await self.redis.hgetall(captcha_key)

        if not data:
            return None
        return CaptchaData(
            message_id=int(data["message_id"]), button_id=data["button_id"]
        )

    async def add_captcha_timeout(
        self, chat_id: int, user_id: int, expires_at: float, captcha_data: CaptchaData
    ) -> None:
        captcha_key = f"captcha:{chat_id}:{user_id}"

        await self.redis.hset(
            captcha_key,
            mapping={k: str(v) for k, v in captcha_data.items()},
        )

        await self.redis.zadd(
            "captcha_timeouts",
            {f"{chat_id}:{user_id}": expires_at},
        )

    async def remove_captcha_timeout(self, chat_id: int, user_id: int) -> None:
        captcha_key = f"captcha:{chat_id}:{user_id}"
        await self.redis.delete(captcha_key)
        await self.redis.zrem("captcha_timeouts", f"{chat_id}:{user_id}")
