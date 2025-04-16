import random
from datetime import datetime, timezone

from sqlalchemy import select
from telethon import TelegramClient

from src.features.anecdote.anecdote_config import ANECDOTE_CONFIG
from src.features.anecdote.models.anecdote_model import AnecdoteModel
from src.features.anecdote.store.anecdote_store import ANECDOTE_STORE, Anecdote
from src.store.db_store import async_session
from src.store.redis_store import REDIS_STORE


class AnecdoteManager:
    def __init__(self, bot: TelegramClient):
        self.bot = bot

    async def __mark_anecdote_used(self, chat_id: int, anecdote: Anecdote) -> None:
        current_time = datetime.now(timezone.utc)
        await REDIS_STORE.set(
            f"{ANECDOTE_CONFIG.REDIS_ANECDOTE_TIME_KEY}:{chat_id}:{anecdote['hash']}",
            current_time.timestamp(),
        )
        async with async_session() as session:
            session.add(
                AnecdoteModel(
                    hash=anecdote["hash"],
                    chat_id=chat_id,
                    timestamp=current_time,
                )
            )
            await session.commit()

    async def get_anecdote(self, chat_id: int) -> Anecdote | None:
        return await self.get_unique_anecdote(chat_id, ANECDOTE_STORE)

    async def get_unique_anecdote(
        self, chat_id: int, anecdote_list: list[Anecdote]
    ) -> Anecdote | None:
        if not anecdote_list:
            return None

        anecdote: Anecdote = random.choice(anecdote_list)

        if await REDIS_STORE.exists(
            f"{ANECDOTE_CONFIG.REDIS_ANECDOTE_TIME_KEY}:{chat_id}:{anecdote['hash']}"
        ):
            anecdote_list.pop(anecdote_list.index(anecdote))
            return await self.get_unique_anecdote(chat_id, anecdote_list)
        async with async_session() as session:
            anecdote_model = await session.scalar(
                select(AnecdoteModel).filter_by(
                    hash=anecdote["hash"],
                )
            )
            if anecdote_model is None:
                await self.__mark_anecdote_used(chat_id, anecdote)
                return anecdote

        anecdote_list.pop(anecdote_list.index(anecdote))
        return await self.get_unique_anecdote(chat_id, anecdote_list)
