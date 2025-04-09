from telethon import TelegramClient
from telethon.events.chataction import ChatAction

from src.features.captcha.store.captcha_store import CAPTCHA_STORE, CaptchaData
from src.features.captcha.utils.captcha_generator import CaptchaGenerator


class UserJoinLeaveHandler:
    def __init__(self, bot: TelegramClient, captcha_generator: CaptchaGenerator):
        self.bot = bot
        self.captcha_generator = captcha_generator

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
        captcha = self.captcha_generator.generate_captcha()
        captcha_button_name = self.captcha_generator.get_captcha_button_name(
            captcha["button_id"]
        )

        message = await event.respond(
            f"Hey, @{event.user.username}! To start chatting in the group, click the **{captcha_button_name}** square below.",
            buttons=captcha["layout"],
        )

        await CAPTCHA_STORE.add_captcha(
            event.chat_id,
            event.user_id,
            CaptchaData(message_id=message.id, button_id=captcha["button_id"]),
        )

    async def __handle_user_leave(self, event: ChatAction.Event) -> None:
        captcha_data = await CAPTCHA_STORE.get_captcha(event.chat_id, event.user_id)
        if not captcha_data:
            return

        await self.bot.delete_messages(event.chat_id, captcha_data["message_id"])
        await CAPTCHA_STORE.remove_captcha(event.chat_id, event.user_id)
