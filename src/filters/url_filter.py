from urllib.error import URLError
from urllib.parse import urlparse

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.i18n.i18n import i18n


class UrlFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            parsed_url = urlparse(message.text)
            hostname = parsed_url.hostname.split('.')
            if 'youtube' not in hostname and 'youtu' not in hostname:
                await message.answer(i18n.translate(message, 'wrong_link'))
                return False
        except URLError:
            await message.answer(i18n.translate(message, 'wrong_link'))
            return False
        return True
