import hashlib
import random
from dataclasses import dataclass
from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.features.anecdote.models.used_anecdote import UsedAnecdote
from src.store.db import Session


@dataclass(frozen=True)
class Anecdote:
    text: str
    hash: str


@lru_cache(maxsize=None)
def _get_anecdote_list() -> list[Anecdote]:
    """Load anecdotes from a file and return a list of them."""
    anecdote_list: list[Anecdote] = []
    with open("anecdotes.txt", "r", encoding="utf-8") as file:
        text_list = [line.strip() for line in file if line.strip()]
        hasher = hashlib.blake2s(digest_size=8)
        for text in text_list:
            text = text.strip()
            hasher.update(text.encode())
            hash = hasher.hexdigest()
            anecdote_list.append(Anecdote(text=text, hash=hash))
    return anecdote_list


async def _get_unused_anecdote_list(chat_id: int) -> list[Anecdote]:
    """Retrieve a list of unused anecdotes for a specific chat ID."""
    async with Session() as session:
        result = await session.scalars(
            select(UsedAnecdote.hash).where(UsedAnecdote.chat_id == chat_id),
        )
    used_hash_list = result.all()
    return [anecdote for anecdote in _get_anecdote_list() if anecdote.hash not in used_hash_list]


async def _mark_anecdote_used(chat_id: int, anecdote: Anecdote) -> None:
    """Mark an anecdote as used for a specific chat ID."""
    async with Session() as session:
        await session.execute(
            insert(UsedAnecdote).values(
                hash=anecdote.hash,
                chat_id=chat_id,
            )
        )
        await session.commit()


async def get_random_anecdote(chat_id: int) -> Anecdote | None:
    """Get a random unused anecdote for a specific chat ID."""
    unused_anecdote_list = await _get_unused_anecdote_list(chat_id)
    if not unused_anecdote_list:
        return None
    unused_anecdote = random.choice(unused_anecdote_list)
    await _mark_anecdote_used(chat_id, unused_anecdote)
    return unused_anecdote
