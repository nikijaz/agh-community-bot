from telethon import TelegramClient

from src.features.captcha.handlers.button_press_handler import ButtonPressHandler
from src.features.captcha.handlers.user_join_leave_handler import UserJoinLeaveHandler
from src.features.captcha.utils.captcha_generator import CaptchaGenerator
from src.features.captcha.utils.captcha_timeout_monitor import CaptchaTimeoutMonitor


class CaptchaFeature:
    def __init__(self, bot: TelegramClient):
        self.bot = bot

    def setup(self) -> None:
        self.setup_captcha_monitor()
        self.setup_captcha_generator()
        self.setup_handlers()

    def setup_captcha_monitor(self) -> None:
        self.captcha_monitor = CaptchaTimeoutMonitor(self.bot)

    def setup_captcha_generator(self) -> None:
        self.captcha_generator = CaptchaGenerator()

    def setup_handlers(self) -> None:
        UserJoinLeaveHandler(self.bot, self.captcha_generator).setup()
        ButtonPressHandler(self.bot).setup()
