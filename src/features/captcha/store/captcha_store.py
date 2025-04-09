import time
from typing import Final, Required, TypedDict

from src.store.redis_store import REDIS_STORE


class CaptchaData(TypedDict):
    message_id: Required[int]
    button_id: Required[str]


class CaptchaStore:
    def __init__(self) -> None:
        pass

    async def get_captcha(self, chat_id: int, user_id: int) -> CaptchaData | None:
        data = await REDIS_STORE.hgetall(f"captcha:{chat_id}:{user_id}")
        if not data:
            return None
        return CaptchaData(
            message_id=int(data["message_id"]), button_id=data["button_id"]
        )

    async def add_captcha(
        self, chat_id: int, user_id: int, captcha_data: CaptchaData
    ) -> None:
        current_time = time.time()
        await REDIS_STORE.hset(
            f"captcha:{chat_id}:{user_id}",
            mapping={k: str(v) for k, v in captcha_data.items()},
        )
        await REDIS_STORE.zadd(
            "captcha_time",
            {f"{chat_id}:{user_id}": current_time},
        )

    async def remove_captcha(self, chat_id: int, user_id: int) -> None:
        await REDIS_STORE.delete(f"captcha:{chat_id}:{user_id}")
        await REDIS_STORE.zrem("captcha_time", f"{chat_id}:{user_id}")


CAPTCHA_STORE: Final = CaptchaStore()
