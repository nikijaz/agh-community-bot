from typing import cast

from telethon.tl.types import Channel

from src.utils.bot import BOT


async def get_chat_name(chat_id: int) -> str:
    """Get the name of a chat by its ID."""
    chat = cast(Channel, await BOT.get_entity(chat_id))
    return chat.title
