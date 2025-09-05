class DownloaderError(Exception):
    """ All Error with download """


class DownloaderWasNotFound(DownloaderError):
    """ Raise when downloader specified in .env not found """
