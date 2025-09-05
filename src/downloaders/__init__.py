from src.config import project_settings
from src.downloaders.downloaders_enum import DownloadersEnum
from src.downloaders.yt_dlp_downloader import YtDlpDownloader
from src.exceptions.downloader_exceptions import DownloaderWasNotFound

match project_settings.DOWNLOADER:
    case DownloadersEnum.YT_DLP.value:
        downloader = YtDlpDownloader()
    case _:
        raise DownloaderWasNotFound('The loader is not in the list of possible ones')
