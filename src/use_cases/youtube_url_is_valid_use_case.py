from urllib.error import URLError
from urllib.parse import urlparse

from src.exceptions.url_parse_exceptions import IsNotYoutubeUrlError
from src.exceptions.url_parse_exceptions import InvalidUrlError


class YoutubeUrlIsValidUseCase(object):
    def execute(self, url: str) -> bool:
        try:
            parsed_url = urlparse(url)

            hostname = parsed_url.hostname.split('.')
            if 'youtube' not in hostname and 'youtu' not in hostname:
                raise IsNotYoutubeUrlError()
            else:
                return True
        except URLError as e:
            raise InvalidUrlError() from e
