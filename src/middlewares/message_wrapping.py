from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.methods import SendMessage
from aiogram.types import TelegramObject, Message

from src.i18n.i18n import i18n


class MessageWrappingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            data["localized_message"] = LocalizedMessageWrapper(event)

        return await handler(event, data)


class LocalizedMessageWrapper:
    def __init__(self, msg: Message):
        self.msg = msg

    async def answer(self, string_key: str, *args, **kwargs) -> SendMessage:
        return self.msg.answer(
            i18n.translate(self.msg.from_user.language_code, string_key),
            *args, **kwargs
        )

    async def reply(self, string_key: str, *args, **kwargs) -> SendMessage:
        return self.msg.reply(
            i18n.translate(self.msg.from_user.language_code, string_key),
            *args, **kwargs
        )
