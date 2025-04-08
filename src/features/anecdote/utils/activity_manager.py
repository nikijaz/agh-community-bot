import asyncio

from redis import Redis
from telethon import TelegramClient

from src.features.anecdote.utils.anecdote_manager import AnecdoteManager
from src.store.redis_store import REDIS_STORE
from src.utils.config import CONFIG


class ActivityManager:
    def __init__(self, bot: TelegramClient, anecdote_manager: AnecdoteManager) -> None:
        self.bot = bot
        self.redis: Redis = REDIS_STORE
        self.anecdote_manager = anecdote_manager

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.__monitor_last_message())

    async def __monitor_last_message(self) -> None:
        while True:
            current_time = self.loop.time()
            inactive_chat_id_list: list[str] = self.redis.zrangebyscore(
                "last_message_times",
                0,
                current_time - CONFIG.INACTIVITY_TIMEOUT,
            )

            for chat_id in inactive_chat_id_list:
                self.loop.create_task(self.__handle_inactivity(int(chat_id)))
                self.redis.zrem("last_message_times", chat_id)

            await asyncio.sleep(5)

    async def __handle_inactivity(self, chat_id: int) -> None:
        await self.bot.send_message(
            chat_id, self.anecdote_manager.get_random_anecdote()
        )

    def bump_activity(self, chat_id: int) -> None:
        self.redis.zadd("last_message_times", {f"{chat_id}": self.loop.time()})
