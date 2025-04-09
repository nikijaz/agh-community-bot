from telethon import TelegramClient
from telethon.events import NewMessage

from src.features.anecdote.utils.activity_manager import ActivityManager


class MessageHandler:
    def __init__(self, bot: TelegramClient, activity_manager: ActivityManager):
        self.bot = bot
        self.activity_manager = activity_manager

    def setup(self):
        self.bot.add_event_handler(self.__handle_message, NewMessage(incoming=True))

    async def __handle_message(self, event: NewMessage.Event):
        await self.activity_manager.bump_activity(event.chat_id)
