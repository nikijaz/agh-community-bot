import asyncio

from telethon.events.callbackquery import CallbackQuery
from telethon.events.chataction import ChatAction

from src.features.captcha.utils import captcha_utils, timeout_utils
from src.utils.bot import BOT
from src.utils.event_handler import handle


def setup() -> None:
    asyncio.create_task(timeout_utils.monitor_captcha_timeout())


@handle(CallbackQuery(pattern="^captcha:"))
async def _handle_captcha_response(event: CallbackQuery.Event) -> None:
    captcha = await captcha_utils.get_captcha(event.chat_id, event.sender_id)
    if captcha is None:
        return
    data = event.data.decode("utf-8")  # <captcha>:<button_id>
    if data.split(":")[1] != captcha.button_id:
        await BOT.kick_participant(event.chat_id, event.sender_id)
    else:
        await BOT.edit_permissions(event.chat_id, event.sender_id, send_messages=True)
    await event.delete()
    await captcha_utils.remove_captcha(event.chat_id, event.sender_id)


@handle(ChatAction(func=lambda e: e.user_joined))
async def _setup_captcha_challenge(event: ChatAction.Event) -> None:
    await BOT.edit_permissions(event.chat_id, event.user_id, send_messages=False)
    layout = captcha_utils.generate_layout()
    button_id = captcha_utils.generate_button_id()
    button_name = captcha_utils.get_button_name(button_id)
    message = await event.respond(
        f"Hey, @{event.user.username}! To start chatting in the group, click the **{button_name}** square below.",
        buttons=layout,
    )
    await captcha_utils.add_captcha(event.chat_id, event.user_id, message.id, button_id)


@handle(ChatAction(func=lambda e: e.user_left))
async def _remove_captcha_on_user_leave(event: ChatAction.Event) -> None:
    captcha = await captcha_utils.get_captcha(event.chat_id, event.user_id)
    if captcha is None:
        return
    await BOT.delete_messages(event.chat_id, captcha.message_id)
    await captcha_utils.remove_captcha(event.chat_id, event.user_id)
