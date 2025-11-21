import os

from aiogram import Router
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from sqlalchemy.exc import IntegrityError

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
    if message.text is None or message.bot is None:
        return
    progress_message = await localized_message.reply('starting_download')

    result_video, video_id = await downloader.download(message.text, progress_message)
    await progress_message.delete()

    async with ChatActionSender.upload_video(message.chat.id, message.bot):
        try:
            msg = await SendVideoUseCase().execute(result_video, message.reply_video)
        except SendingError:
            return

    if result_video.video_file is not None:
        video_file_id = msg.video.file_id
        try:
            await video_service.create(VideoCreate(id=video_id, file_id=video_file_id)) # pyright: ignore[reportArgumentType]

            os.remove(result_video.video_file)
        except IntegrityError:
            return
