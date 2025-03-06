from dataclasses import dataclass

from aiogram.types import InputFile


@dataclass
class VideoToSend:
    file: str | InputFile
    caption: str
    width: int | None = None
    height: int | None = None
    duration: int | None = None
    cover: str | None = None
    supports_streaming: bool = True
