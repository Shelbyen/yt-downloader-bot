from src.services.base_service import BaseService
from ..repositories.video_repository import video_repository


class VideoService(BaseService):
    async def exist(self, video_id: str) -> bool:
        return await self.repository.exist(video_id)


video_service = VideoService(repository=video_repository)
