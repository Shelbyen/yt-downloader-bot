from src.config.database.db_helper import db_helper
from src.models.video_model import VideoModel
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository
from ..schemas.video_schema import VideoCreate, VideoUpdate


class VideoRepository(SqlAlchemyRepository[VideoModel, VideoCreate, VideoUpdate]):
    ...


video_repository = VideoRepository(model=VideoModel, db_session=db_helper.get_db_session)
