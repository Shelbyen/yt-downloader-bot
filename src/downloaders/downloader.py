from abc import ABC, abstractmethod

from src.schemas.video_to_send_schema import VideoToSend


class Downloader(ABC):
    """ Abstract downloader """
    @abstractmethod
    async def download(self, url: str, *args, **kwargs) -> tuple[VideoToSend, str] | None:
        """ Download video using link """
        raise NotImplementedError
