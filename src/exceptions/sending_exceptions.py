class SendingError(Exception):
    key: str = "sending_error"

class BigFileError(SendingError):
    key: str = "video_too_big"

class CoverError(SendingError):
    key: str = "video_cover_error"
