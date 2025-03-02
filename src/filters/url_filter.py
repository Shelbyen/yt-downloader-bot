from urllib.error import URLError
from urllib.parse import urlparse

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.i18n.i18n import i18n


class UrlFilter(BaseFilter):
    def __init__(self, answer_when_wrong: bool = True):
        self.answer_when_wrong = answer_when_wrong

    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        try:
            parsed_url = urlparse(message.text)
            hostname = parsed_url.hostname.split('.')
            if 'youtube' not in hostname and 'youtu' not in hostname:
                if self.answer_when_wrong:
                    await message.answer(i18n.translate(message, 'wrong_link'))
                return False
        except URLError:
            if self.answer_when_wrong:
                await message.answer(i18n.translate(message, 'wrong_link'))
            return False
        return True
