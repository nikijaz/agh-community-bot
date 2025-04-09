from telethon import TelegramClient
from telethon.events.callbackquery import CallbackQuery

from src.features.captcha.utils.captcha_manager import CaptchaManager


class ButtonPressHandler:
    def __init__(self, bot: TelegramClient, captcha_manager: CaptchaManager):
        self.bot = bot
        self.captcha_manager = captcha_manager

    def setup(self) -> None:
        self.bot.add_event_handler(
            self.__handle_button_press, CallbackQuery(data="buttonCaptcha")
        )

    async def __handle_button_press(self, event: CallbackQuery.Event) -> None:
        await self.bot.edit_permissions(
            event.chat_id, event.sender_id, send_messages=True
        )
        await event.delete()
        await self.captcha_manager.remove_captcha_timeout(
            event.chat_id, event.sender_id
        )
