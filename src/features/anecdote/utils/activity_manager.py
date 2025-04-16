import asyncio
import time

from telethon import TelegramClient

from src.features.anecdote.anecdote_config import ANECDOTE_CONFIG
from src.features.anecdote.utils.anecdote_manager import AnecdoteManager
from src.store.redis_store import REDIS_STORE


class ActivityManager:
    def __init__(self, bot: TelegramClient, anecdote_manager: AnecdoteManager) -> None:
        self.bot = bot
        self.redis = REDIS_STORE
        self.anecdote_manager = anecdote_manager

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.__monitor_last_message())

    async def __monitor_last_message(self) -> None:
        while True:
            current_time = time.time()
            async for key in self.redis.scan_iter(
                f"{ANECDOTE_CONFIG.REDIS_ACTIVE_TIME_KEY}:*"
            ):
                value = await self.redis.get(key)
                chat_id = int(key.split(":")[1])
                if not value:
                    continue

                last_activity_time = float(value)
                if (
                    last_activity_time
                    > current_time
                    - await ANECDOTE_CONFIG.INACTIVITY_TIMEOUT.get(chat_id)
                ):
                    continue

                self.loop.create_task(self.__handle_inactivity(chat_id))
                await self.redis.delete(key)

            await asyncio.sleep(5)

    async def __handle_inactivity(self, chat_id: int) -> None:
        anecdote = await self.anecdote_manager.get_anecdote(chat_id)
        if not anecdote:
            await self.bot.send_message(
                chat_id,
                "I was gonna tell a joke, but then I remembered I'm a bot with limitations.",
            )
            return
        await self.bot.send_message(chat_id, anecdote["text"])

    async def bump_activity(self, chat_id: int) -> None:
        await self.redis.set(
            f"{ANECDOTE_CONFIG.REDIS_ACTIVE_TIME_KEY}:{chat_id}", str(time.time())
        )
