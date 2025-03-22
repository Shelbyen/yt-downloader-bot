from abc import ABC, abstractmethod

from src.schemas.video_to_send_schema import VideoToSend


class Downloader(ABC):
    @abstractmethod
    def download(self, url: str, *args, **kwargs) -> tuple[VideoToSend, str] | None:
        raise NotImplementedError
