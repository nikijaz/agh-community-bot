from telethon import TelegramClient

from src.features.anecdote.handlers.message_handler import MessageHandler
from src.features.anecdote.utils.activity_manager import ActivityManager
from src.features.anecdote.utils.anecdote_manager import AnecdoteManager


class AnecdoteFeature:
    def __init__(self, bot: TelegramClient):
        self.bot = bot

    def setup(self):
        self.setup_anecdote_manager()
        self.setup_activity_manager()
        self.setup_handlers()

    def setup_anecdote_manager(self):
        self.anecdote_manager = AnecdoteManager(self.bot)

    def setup_activity_manager(self):
        self.activity_manager = ActivityManager(self.bot, self.anecdote_manager)

    def setup_handlers(self):
        MessageHandler(self.bot, self.activity_manager).setup()
