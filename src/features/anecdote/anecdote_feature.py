import asyncio

from telethon.events.newmessage import NewMessage

from src.features.anecdote.utils import activity_utils
from src.utils.event_handler import handle


def setup() -> None:
    """Setup the anecdote feature."""
    asyncio.create_task(activity_utils.monitor_activity())


@handle(NewMessage())
async def _handle_activity(event: NewMessage.Event) -> None:
    """Handle new messages to update activity."""
    await activity_utils.bump_activity(event.chat_id)
