from urllib.error import URLError
from urllib.parse import urlparse

from aiogram.types import MessageEntity

from src.exceptions.url_parse_exceptions import IsNotYoutubeUrlError
from src.exceptions.url_parse_exceptions import InvalidUrlError


class YoutubeUrlIsValidUseCase(object):
    def execute(self, message_text: str | None, entities: list[MessageEntity] | None) -> bool:
        urls = [item.extract_from(message_text or '') for item in (entities or []) if item.type == 'url'] or []
        if len(urls) == 0:
            raise InvalidUrlError()
        url = urls[0]

        try:
            parsed_url = urlparse(url)

            hostname = parsed_url.hostname.split('.')
            if 'youtube' not in hostname and 'youtu' not in hostname:
                raise IsNotYoutubeUrlError()
            else:
                return True
        except URLError as e:
            raise InvalidUrlError() from e
