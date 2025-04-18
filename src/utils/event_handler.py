from typing import Awaitable, Callable, TypeVar

from telethon.events.common import EventBuilder, EventCommon

from src.utils.bot import BOT

T = TypeVar("T", bound=EventBuilder)
V = TypeVar("V", bound=EventCommon)
EventHandler = Callable[[V], Awaitable[None]]


def handle(event: T) -> Callable[[EventHandler[V]], EventHandler[V]]:
    """Decorator to handle events."""

    def decorator(func: EventHandler[V]) -> EventHandler[V]:
        BOT.on(event)(func)
        return func

    return decorator
