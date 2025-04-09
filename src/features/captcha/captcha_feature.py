from telethon import TelegramClient

from src.features.captcha.handlers.button_press_handler import ButtonPressHandler
from src.features.captcha.handlers.user_join_leave_handler import UserJoinLeaveHandler
from src.features.captcha.utils.captcha_manager import CaptchaManager


class CaptchaFeature:
    def __init__(self, bot: TelegramClient):
        self.bot = bot

    def setup(self) -> None:
        self.setup_captcha_manager()
        self.setup_handlers()

    def setup_captcha_manager(self) -> None:
        self.captcha_manager = CaptchaManager(self.bot)

    def setup_handlers(self) -> None:
        UserJoinLeaveHandler(self.bot, self.captcha_manager).setup()
        ButtonPressHandler(self.bot, self.captcha_manager).setup()
