import random

from telethon import TelegramClient

from src.features.anecdote.store.anecdote_store import ANECDOTE_STORE, Anecdote


class AnecdoteManager:
    def __init__(self, bot: TelegramClient):
        self.bot = bot
        self.anecdote_list: list[Anecdote] = ANECDOTE_STORE

    def get_random_anecdote(self) -> str:
        return random.choice(self.anecdote_list)["text"]
