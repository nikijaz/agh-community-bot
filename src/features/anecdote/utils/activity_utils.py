import asyncio

from sqlalchemy import and_, or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.functions import current_timestamp

from src.features.anecdote.anecdote_config import ANECDOTE_CONFIG
from src.features.anecdote.models.last_message import LastMessage
from src.features.anecdote.utils import anecdote_utils
from src.per_chat_config.models.config_entry import ConfigEntry
from src.store.db import Session
from src.utils.bot import BOT
from src.utils.postgres_utils import interval


async def _handle_inactivity(chat_id: int) -> None:
    """Handle inactivity by sending a random anecdote."""
    anecdote = await anecdote_utils.get_random_anecdote(chat_id)
    if anecdote is None:
        await BOT.send_message(chat_id, "I was gonna tell a joke, but then I remembered I'm a bot with limitations.")
        return
    await BOT.send_message(chat_id, anecdote.text)


async def _check_for_inactivity() -> None:
    """Check for inactive chats and handle them."""
    async with Session() as session:
        time_lasted = current_timestamp() - LastMessage.updated_at
        inactivity_condition_default = and_(
            ConfigEntry.key.is_(None),
            time_lasted > interval(ANECDOTE_CONFIG.INACTIVITY_TIMEOUT.default),
        )
        inactivity_condition_custom = and_(
            ConfigEntry.key == ANECDOTE_CONFIG.INACTIVITY_TIMEOUT.key,
            time_lasted > interval(ConfigEntry.value),
        )
        inactivity_condition = or_(inactivity_condition_default, inactivity_condition_custom)
        result = await session.scalars(
            select(LastMessage)
            .join(
                ConfigEntry,
                ConfigEntry.chat_id == LastMessage.chat_id,
                isouter=True,
            )
            .where(inactivity_condition)
        )
    last_message_list = result.all()
    for last_message in last_message_list:
        await _handle_inactivity(last_message.chat_id)
        async with Session() as session:
            await session.delete(last_message)
            await session.commit()


async def monitor_activity() -> None:
    """Continuously monitor chat activity."""
    while True:
        await _check_for_inactivity()
        await asyncio.sleep(ANECDOTE_CONFIG.ACTIVITY_TIMEOUT_INTERVAL)


async def bump_activity(chat_id: int) -> None:
    """Update the activity timestamp for a chat."""
    async with Session() as session:
        await session.execute(
            insert(LastMessage)
            .values(chat_id=chat_id)
            .on_conflict_do_update(
                index_elements=[LastMessage.chat_id],
                set_={LastMessage.updated_at: current_timestamp()},
            )
        )
        await session.commit()
