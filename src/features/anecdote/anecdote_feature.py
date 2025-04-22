import asyncio

from sqlalchemy import delete, select
from telethon import Button
from telethon.events import StopPropagation
from telethon.events.callbackquery import CallbackQuery
from telethon.events.newmessage import NewMessage
from telethon.tl.types import Message

from src.features.anecdote.models.anecdote import Anecdote
from src.features.anecdote.utils import activity_utils
from src.features.config.models.chat_owner import ChatOwner
from src.store.db import Session
from src.utils import api_utils
from src.utils.bot import BOT
from src.utils.event_handler import handle


def setup() -> None:
    """Setup the anecdote feature."""
    asyncio.create_task(activity_utils.monitor_activity())


@handle(NewMessage())
async def _handle_anecdote_submission(event: NewMessage.Event) -> None:
    """Handle new messages to add anecdotes."""
    message: Message = event.message
    if message.from_id is not None or message.message.startswith("/"):
        return  # Ignore private messages and commands

    async with Session() as session:
        result = await session.scalars(
            select(ChatOwner).where(ChatOwner.owner_id == event.peer_id.user_id),
        )
    chat_owner_list = result.all()
    if not chat_owner_list:
        await event.respond(
            "You are either not the owner of any chat or you have not synced any chat yet. Try to use /sync in a chat you own."
        )
        raise StopPropagation

    await event.reply(
        "Choose a chat in which to add the anecdote",
        buttons=[
            Button.inline(await api_utils.get_chat_name(chat_owner.chat_id), data=f"add_anecdote:{chat_owner.chat_id}")
            for chat_owner in chat_owner_list
        ],
    )
    raise StopPropagation


@handle(CallbackQuery(pattern="^add_anecdote:"))
async def _handle_anecdote_creation(event: CallbackQuery.Event) -> None:
    """Handle the creation of an anecdote."""
    bot_message = await event.get_message()
    anecdote_message = await BOT.get_messages(event.chat_id, ids=bot_message.reply_to.reply_to_msg_id)
    assert isinstance(anecdote_message, Message)
    chat_id = int(event.data.decode("utf-8").split(":")[1])

    anecdote = Anecdote(chat_id=chat_id, text=anecdote_message.message)
    async with Session() as session:
        session.add(anecdote)
        await session.commit()

    await BOT.edit_message(
        event.chat_id,
        bot_message.id,
        f"Anecdote added!\nChat: `{await api_utils.get_chat_name(chat_id)}`\nID: `{anecdote.id}`",
        buttons=[
            Button.inline("Delete", data=f"remove_anecdote:{anecdote.id}"),
        ],
    )
    raise StopPropagation


@handle(CallbackQuery(pattern="^remove_anecdote:"))
async def _handle_anecdote_removal(event: CallbackQuery.Event) -> None:
    """Handle the removal of an anecdote."""
    message = await event.get_message()
    anecdote_message = await BOT.get_messages(event.chat_id, ids=message.reply_to.reply_to_msg_id)
    assert isinstance(anecdote_message, Message)
    anecdote_id = int(event.data.decode("utf-8").split(":")[1])

    async with Session() as session:
        await session.execute(delete(Anecdote).where(Anecdote.id == anecdote_id))
        await session.commit()

    await BOT.delete_messages(
        event.chat_id,
        [message.id, anecdote_message.id],
    )
    raise StopPropagation


@handle(NewMessage())
async def _handle_activity(event: NewMessage.Event) -> None:
    """Handle new messages to update activity."""
    message: Message = event.message
    if message.from_id is None or message.message.startswith("/"):
        return  # Ignore private messages and commands
    await activity_utils.bump_activity(event.chat_id)
