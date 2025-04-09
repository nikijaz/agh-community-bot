import time

from telethon import Button, TelegramClient
from telethon.events.chataction import ChatAction

from src.features.captcha.utils.captcha_manager import CaptchaManager


class UserJoinLeaveHandler:
    def __init__(self, bot: TelegramClient, captcha_manager: CaptchaManager):
        self.bot = bot
        self.captcha_manager = captcha_manager

    def setup(self) -> None:
        self.bot.add_event_handler(
            self.__handle_user_join,
            ChatAction(func=lambda e: e.user_joined),
        )
        self.bot.add_event_handler(
            self.__handle_user_leave,
            ChatAction(func=lambda e: e.user_left),
        )

    async def __handle_user_join(self, event: ChatAction.Event) -> None:
        await self.bot.edit_permissions(
            event.chat_id, event.user_id, send_messages=False
        )
        message = await event.respond(
            f"Hey, @{event.user.username}! To start chatting in the group, click the button below.",
            buttons=[Button.inline("I'm not a robot", data="buttonCaptcha")],
        )
        await self.captcha_manager.add_captcha_timeout(
            event.chat_id,
            event.user_id,
            (time.time() + 5),
            {"message_id": message.id},
        )

    async def __handle_user_leave(self, event: ChatAction.Event) -> None:
        captcha_data = await self.captcha_manager.get_captcha_data(
            event.chat_id, event.user_id
        )
        if captcha_data:
            await self.bot.delete_messages(event.chat_id, captcha_data["message_id"])
            await self.captcha_manager.remove_captcha_timeout(
                event.chat_id, event.user_id
            )
