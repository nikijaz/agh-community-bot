import asyncio
import time

from telethon import TelegramClient

from src.features.captcha.store.captcha_store import CaptchaData
from src.store.redis_store import REDIS_STORE
from src.utils.config import CONFIG


class CaptchaTimeoutMonitor:
    def __init__(self, bot: TelegramClient):
        self.bot = bot

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.__monitor_captcha_timeout())

    async def __monitor_captcha_timeout(self) -> None:
        while True:
            current_time = time.time()
            expired_keys: list[str] = await REDIS_STORE.zrangebyscore(
                "captcha_time", 0, current_time - CONFIG.CAPTCHA_TIMEOUT
            )

            for key in expired_keys:
                chat_id, user_id = key.split(":")
                captcha_key = f"captcha:{chat_id}:{user_id}"

                data = await REDIS_STORE.hgetall(captcha_key)
                captcha_data = CaptchaData(
                    message_id=int(data["message_id"]), button_id=data["button_id"]
                )
                self.loop.create_task(
                    self.__handle_captcha_timeout(
                        int(chat_id), int(user_id), captcha_data
                    )
                )

                await REDIS_STORE.delete(captcha_key)
                await REDIS_STORE.zrem("captcha_time", key)

            await asyncio.sleep(5)

    async def __handle_captcha_timeout(
        self, chat_id: int, user_id: int, captcha_data: CaptchaData
    ) -> None:
        message_id = captcha_data["message_id"]

        await self.bot.delete_messages(chat_id, message_id)
        await self.bot.kick_participant(chat_id, user_id)
