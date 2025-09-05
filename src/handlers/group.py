import os

from aiogram import Router
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from src.downloaders import downloader
from src.exceptions.sending_exceptions import SendingError
from src.filters.url_filter import UrlFilter
from src.middlewares.message_wrapping import LocalizedMessageWrapper
from src.schemas.video_schema import VideoCreate
from src.services.video_service import video_service
from src.use_cases.send_video_use_case import SendVideoUseCase

router = Router()
all_media_dir = 'res/yt-dir'


@router.message(UrlFilter(answer_when_wrong=False))
async def check_message(message: Message, localized_message: LocalizedMessageWrapper):
    progress_message = await localized_message.reply('starting_download')

    result_video, video_id = await downloader.download(message.text, progress_message) # type: ignore
    await progress_message.delete()

    async with ChatActionSender.upload_video(message.from_user.id, message.bot): # type: ignore
        try:
            msg = await SendVideoUseCase().execute(result_video, message.reply_video)
        except SendingError:
            return

    if not isinstance(result_video.video, str):
        video_file_id = msg.video.file_id

        await video_service.create(VideoCreate(id=video_id, file_id=video_file_id)) # type: ignore
        
        os.remove(os.path.join(all_media_dir, result_video.cover + '.mp4'))
