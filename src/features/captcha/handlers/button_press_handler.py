from telethon import TelegramClient
from telethon.events.callbackquery import CallbackQuery

from src.features.captcha.store.captcha_store import CAPTCHA_STORE


class ButtonPressHandler:
    def __init__(self, bot: TelegramClient):
        self.bot = bot

    def setup(self) -> None:
        self.bot.add_event_handler(
            self.__handle_button_press, CallbackQuery(pattern="^captcha:")
        )

    async def __handle_button_press(self, event: CallbackQuery.Event) -> None:
        captcha_data = await CAPTCHA_STORE.get_captcha(event.chat_id, event.sender_id)
        if not captcha_data:
            return

        data = event.data.decode("utf-8")  # captcha:button_id
        if data.split(":")[1] != captcha_data["button_id"]:
            await self.bot.kick_participant(event.chat_id, event.sender_id)
        else:
            await self.bot.edit_permissions(
                event.chat_id, event.sender_id, send_messages=True
            )

        await event.delete()
        await CAPTCHA_STORE.remove_captcha(event.chat_id, event.sender_id)
