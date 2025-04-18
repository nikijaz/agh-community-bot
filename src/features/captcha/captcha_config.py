from typing import Final

from src.per_chat_config.config_field import ConfigField


class CaptchaConfig:
    """Configuration for the Captcha feature."""

    REDIS_CAPTCHA_TIME_KEY = "captcha_time"
    REDIS_CAPTCHA_DATA_KEY = "captcha_data"

    CAPTCHA_TIMEOUT = ConfigField(
        key="captcha_timeout",
        description="Time in seconds before kicking a user",
        default=5,
    )


CAPTCHA_CONFIG: Final = CaptchaConfig()
