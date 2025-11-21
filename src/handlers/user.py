import os

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from sqlalchemy.exc import IntegrityError

from src.downloaders import downloader
from src.exceptions.sending_exceptions import BigFileError, SendingError
from src.filters.url_filter import UrlFilter
from src.middlewares.message_wrapping import LocalizedMessageWrapper
from src.schemas.video_schema import VideoCreate
from src.services.video_service import video_service
from src.use_cases.send_video_use_case import SendVideoUseCase

router = Router()
all_media_dir = "res/yt-dir"


class DownloadingVideo(StatesGroup):
    """States for download"""

    download_in_progress = State()


@router.message(Command("start"))
async def start_message(_: Message, localized_message: LocalizedMessageWrapper):
    await localized_message.answer("start_message")


@router.message(StateFilter(None), UrlFilter())
async def get_link(message: Message, localized_message: LocalizedMessageWrapper):
    if message.text is None or message.bot is None:
        return
    progress_message = await localized_message.answer("starting_download")

    # downloader.download_now_id[message.from_user.id] = 'starting'
    # tt = await asyncio.gather(send_progress(message), download(message.text, progress_message))
    result_video, video_id = await downloader.download(message.text, progress_message)
    await progress_message.delete()

    async with ChatActionSender.upload_video(message.chat.id, message.bot):
        try:
            msg = await SendVideoUseCase().execute(result_video, message.answer_video)
        except BigFileError:
            await localized_message.answer("video_too_big")
            if result_video.video_file is not None:
                os.remove(result_video.video_file)
            return
        except SendingError:
            await localized_message.answer("sending_error")
            return

    if result_video.video_file is not None:
        video_file_id = msg.video.file_id
        if not await video_service.exist(video_id):
            try:
                await video_service.create(
                    VideoCreate(
                        id=video_id, file_id=video_file_id
                    )  # pyright: ignore[reportArgumentType]
                )
            except IntegrityError:
                return
        os.remove(result_video.video_file)
