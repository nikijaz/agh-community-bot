import asyncio
import time

from telethon import TelegramClient

from src.features.captcha.captcha_config import CAPTCHA_CONFIG
from src.features.captcha.store.captcha_store import CaptchaData
from src.store.redis_store import REDIS_STORE


class CaptchaTimeoutMonitor:
    def __init__(self, bot: TelegramClient):
        self.bot = bot

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.__monitor_captcha_timeout())

    async def __monitor_captcha_timeout(self) -> None:
        while True:
            current_time = time.time()
            async for key in REDIS_STORE.scan_iter(
                f"{CAPTCHA_CONFIG.REDIS_CAPTCHA_TIME_KEY}:*"
            ):
                value = await REDIS_STORE.get(key)
                chat_id = int(key.split(":")[1])
                user_id = int(key.split(":")[2])
                if not value:
                    continue

                data = await REDIS_STORE.hgetall(
                    f"{CAPTCHA_CONFIG.REDIS_CAPTCHA_DATA_KEY}:{chat_id}:{user_id}"
                )
                captcha_data = CaptchaData(
                    message_id=int(data["message_id"]), button_id=data["button_id"]
                )

                captcha_time = float(value)
                if (
                    captcha_time
                    > current_time - await CAPTCHA_CONFIG.CAPTCHA_TIMEOUT.get(chat_id)
                ):
                    continue

                self.loop.create_task(
                    self.__handle_captcha_timeout(chat_id, user_id, captcha_data)
                )

                await REDIS_STORE.delete(key)
                await REDIS_STORE.delete(
                    f"{CAPTCHA_CONFIG.REDIS_CAPTCHA_DATA_KEY}:{chat_id}:{user_id}"
                )

            await asyncio.sleep(5)

    async def __handle_captcha_timeout(
        self, chat_id: int, user_id: int, captcha_data: CaptchaData
    ) -> None:
        message_id = captcha_data["message_id"]

        await self.bot.delete_messages(chat_id, message_id)
        await self.bot.kick_participant(chat_id, user_id)
