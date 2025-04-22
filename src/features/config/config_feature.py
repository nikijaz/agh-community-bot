from sqlalchemy.dialects.postgresql import insert
from telethon.events import StopPropagation
from telethon.events.newmessage import NewMessage
from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantsAdmins

from src.features.config.models.chat_owner import ChatOwner
from src.store.db import Session
from src.utils.bot import BOT
from src.utils.event_handler import handle


def setup() -> None:
    pass


@handle(NewMessage(pattern="/sync"))
async def _handle_sync(event: NewMessage.Event) -> None:
    """Handle the /sync command to sync the chat owner."""
    owner = [
        participant
        for participant in await BOT.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
        if type(participant.participant) is ChannelParticipantCreator
    ][0]

    if event.from_id.user_id != owner.id:
        await event.reply("You are not the owner of this chat.")
        await BOT.delete_messages(event.chat_id, event.message.id)
        raise StopPropagation

    async with Session() as session:
        await session.execute(
            insert(ChatOwner)
            .values(chat_id=event.chat_id, owner_id=owner.id)
            .on_conflict_do_update(index_elements=["chat_id"], set_={"owner_id": owner.id}),
        )
        await session.commit()
    await BOT.delete_messages(event.chat_id, event.message.id)
    raise StopPropagation
