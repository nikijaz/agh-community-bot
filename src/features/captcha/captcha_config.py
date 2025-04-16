from typing import Final

from src.config.config_entry import ConfigEntry


class CaptchaConfig:
    REDIS_CAPTCHA_TIME_KEY = "captcha_time"
    REDIS_CAPTCHA_DATA_KEY = "captcha_data"

    CAPTCHA_TIMEOUT = ConfigEntry(
        key="captcha_timeout",
        description="Time in seconds before kicking a user",
        default=60,
    )


CAPTCHA_CONFIG: Final = CaptchaConfig()
