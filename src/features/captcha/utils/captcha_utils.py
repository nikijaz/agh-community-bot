import random

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from telethon import Button
from telethon.tl.types import KeyboardButtonCallback

from src.features.captcha.models.captcha import Captcha
from src.store.db import Session

BUTTONS = {
    "red": Button.inline("\U0001f7e5", data="captcha:red"),
    "yellow": Button.inline("\U0001f7e8", data="captcha:yellow"),
    "green": Button.inline("\U0001f7e9", data="captcha:green"),
    "blue": Button.inline("\U0001f7e6", data="captcha:blue"),
}


async def get_captcha(chat_id: int, user_id: int) -> Captcha | None:
    """Get captcha data from the database."""
    async with Session() as session:
        result = await session.scalar(select(Captcha).where(Captcha.chat_id == chat_id, Captcha.user_id == user_id))
    return result


async def add_captcha(chat_id: int, user_id: int, message_id: int, button_id: str) -> None:
    """Add captcha data to the database."""
    async with Session() as session:
        await session.execute(
            insert(Captcha).values(
                chat_id=chat_id,
                user_id=user_id,
                message_id=message_id,
                button_id=button_id,
            )
        )
        await session.commit()


async def remove_captcha(chat_id: int, user_id: int) -> None:
    """Remove captcha data from the database."""
    async with Session() as session:
        await session.execute(delete(Captcha).where(Captcha.chat_id == chat_id, Captcha.user_id == user_id))
        await session.commit()


def generate_layout() -> list[list[KeyboardButtonCallback]]:
    """Generate a random captcha layout."""
    random_button_list = random.sample(list(BUTTONS.values()), 4)
    return [random_button_list[:2], random_button_list[2:]]


def generate_button_id() -> str:
    """Generate a random button ID."""
    return random.choice(list(BUTTONS.keys()))


def get_button_name(button_id: str) -> str:
    """Get the name of the captcha button based on its ID."""
    return {
        "red": "red",
        "yellow": "yellow",
        "green": "green",
        "blue": "blue",
    }[button_id]  # Will be later used for i18n
