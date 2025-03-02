from src.services.base_service import BaseService
from ..repositories.video_repository import video_repository


class VideoService(BaseService):
    ...


video_service = VideoService(repository=video_repository)
