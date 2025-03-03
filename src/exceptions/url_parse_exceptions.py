class UrlParseError(Exception):
    key: str = "url_parse_error"

class IsNotYoutubeUrlError(UrlParseError):
    key: str = "is_not_youtube_url_error"

class InvalidUrlError(UrlParseError):
    key: str = "invalid_url_error"

class IsNotVideoUrlError(UrlParseError):
    key: str = "is_not_video_url_error"
