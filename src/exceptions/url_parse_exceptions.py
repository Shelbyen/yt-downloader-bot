class UrlParseError(Exception):
    """ All errors of url parse """
    key: str = "url_parse_error"

class IsNotYoutubeUrlError(UrlParseError):
    """ Raise when link don`t have youtube/yoube in host name """
    key: str = "is_not_youtube_url_error"

class InvalidUrlError(UrlParseError):
    """ Raise when message don`t have a link """
    key: str = "invalid_url_error"

class IsNotVideoUrlError(UrlParseError):
    """ Raise when link does not lead to the video """
    key: str = "is_not_video_url_error"
