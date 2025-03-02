from pydantic import BaseModel


class VideoBase(BaseModel):
    id: str
    file_id: str


class VideoCreate(VideoBase):
    pass


class VideoUpdate(VideoBase):
    pass


class VideoResponse(VideoBase):
    pass


class VideoListResponse(VideoBase):
    pass
