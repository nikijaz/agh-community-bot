import random

from sqlalchemy import and_, select

from src.features.anecdote.models.anecdote import Anecdote
from src.store.db import Session


async def _get_unused_anecdote_list(chat_id: int) -> list[Anecdote]:
    """Retrieve a list of unused anecdotes for a specific chat ID."""
    async with Session() as session:
        result = await session.scalars(
            select(Anecdote).where(
                and_(
                    Anecdote.chat_id == chat_id,
                    Anecdote.used.is_(False),
                ),
            ),
        )
    return list(result.all())


async def _mark_anecdote_used(anecdote: Anecdote) -> None:
    """Mark an anecdote as used."""
    async with Session() as session:
        anecdote.used = True
        await session.commit()


async def get_random_anecdote(chat_id: int) -> Anecdote | None:
    """Get a random unused anecdote for a specific chat ID."""
    unused_anecdote_list = await _get_unused_anecdote_list(chat_id)
    if not unused_anecdote_list:
        return None
    unused_anecdote = random.choice(unused_anecdote_list)
    await _mark_anecdote_used(unused_anecdote)
    return unused_anecdote
