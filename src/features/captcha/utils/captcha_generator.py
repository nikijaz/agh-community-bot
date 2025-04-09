import random
from typing import TypedDict

from telethon import Button
from telethon.tl.types import KeyboardButtonCallback


class Captcha(TypedDict):
    button_id: str
    layout: list[list[KeyboardButtonCallback]]


class CaptchaGenerator:
    def __init__(self) -> None:
        self.buttons = {
            "red": Button.inline("\U0001f7e5", data="captcha:red"),
            "yellow": Button.inline("\U0001f7e8", data="captcha:yellow"),
            "green": Button.inline("\U0001f7e9", data="captcha:green"),
            "blue": Button.inline("\U0001f7e6", data="captcha:blue"),
        }

    def generate_captcha(self) -> Captcha:
        buttons = list(self.buttons.values())
        random.shuffle(buttons)
        button_id = random.choice(list(self.buttons.keys()))
        layout = [
            [buttons[0], buttons[1]],
            [buttons[2], buttons[3]],
        ]
        return Captcha(
            button_id=button_id,
            layout=layout,
        )

    def get_captcha_button_name(self, button_id: str) -> str:
        return {
            "red": "red",
            "yellow": "yellow",
            "green": "green",
            "blue": "blue",
        }[button_id]  # Will be later used for i18n
