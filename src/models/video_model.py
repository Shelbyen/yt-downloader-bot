from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base


class VideoModel(Base):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    file_id: Mapped[str]
