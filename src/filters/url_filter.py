from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.exceptions.url_parse_exceptions import UrlParseError
from src.i18n.i18n import i18n
from src.use_cases.youtube_url_is_valid_use_case import YoutubeUrlIsValidUseCase


class UrlFilter(BaseFilter):
    def __init__(self, answer_when_wrong: bool = True):
        self.answer_when_wrong = answer_when_wrong

    async def __call__(self, message: Message) -> bool:
        url = message.text

        try:
            YoutubeUrlIsValidUseCase.execute(url)
        except UrlParseError as exception:
            if self.answer_when_wrong:
                warning_text = i18n.translate(message.from_user.language_code, exception.key)
                message.answer(warning_text)
            return False
        return True
