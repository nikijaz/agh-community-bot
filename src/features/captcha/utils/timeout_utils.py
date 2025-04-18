import asyncio

from sqlalchemy import and_, or_, select
from sqlalchemy.sql.functions import current_timestamp

from src.features.captcha.captcha_config import CAPTCHA_CONFIG
from src.features.captcha.models.captcha import Captcha
from src.per_chat_config.models.config_entry import ConfigEntry
from src.store.db import Session
from src.utils.bot import BOT
from src.utils.postgres_utils import interval


async def _handle_captcha_timeout(captcha: Captcha) -> None:
    """Handle captcha timeout by deleting the message and kicking the user."""
    await BOT.delete_messages(captcha.chat_id, captcha.message_id)
    await BOT.kick_participant(captcha.chat_id, captcha.user_id)


async def _check_for_captcha_timeout() -> None:
    """Check for captcha timeouts and handle them."""
    async with Session() as session:
        time_lasted = current_timestamp() - Captcha.inserted_at
        inactivity_condition_default = and_(
            ConfigEntry.key.is_(None),
            time_lasted > interval(CAPTCHA_CONFIG.CAPTCHA_TIMEOUT.default),
        )
        inactivity_condition_custom = and_(
            ConfigEntry.key == CAPTCHA_CONFIG.CAPTCHA_TIMEOUT.key,
            time_lasted > interval(ConfigEntry.value),
        )
        inactivity_condition = or_(inactivity_condition_default, inactivity_condition_custom)
        result = await session.scalars(
            select(Captcha)
            .join(
                ConfigEntry,
                ConfigEntry.chat_id == Captcha.chat_id,
                isouter=True,
            )
            .where(inactivity_condition)
        )
    captcha_list = result.all()
    for captcha in captcha_list:
        await _handle_captcha_timeout(captcha)
        async with Session() as session:
            await session.delete(captcha)
            await session.commit()


async def monitor_captcha_timeout() -> None:
    """Continuously monitor for captcha timeouts."""
    while True:
        await _check_for_captcha_timeout()
        await asyncio.sleep(5)
