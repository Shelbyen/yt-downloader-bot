class SendingError(Exception):
    """ All sending errors """
    key: str = "sending_error"

class BigFileError(SendingError):
    """ Raise when bot trying to send a file larger than 2GB"""
    key: str = "video_too_big"

class CoverError(SendingError):
    """ Raise when bot can't attach a cover """
    key: str = "video_cover_error"
