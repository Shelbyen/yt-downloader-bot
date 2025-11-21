from sqlalchemy import select
from src.config.database.db_helper import db_helper
from src.models.video_model import VideoModel
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository
from ..schemas.video_schema import VideoCreate, VideoUpdate


class VideoRepository(SqlAlchemyRepository[VideoModel, VideoCreate, VideoUpdate]):
    async def exist(self, video_id) -> bool:
        stmt = select(self.model).where(self.model.id == video_id)
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return result.scalar() is not None


video_repository = VideoRepository(model=VideoModel, db_session=db_helper.get_db_session)
