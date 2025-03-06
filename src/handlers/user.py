import asyncio
import os

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from src.exceptions.sending_exceptions import BigFileError, SendingError
from src.filters.url_filter import UrlFilter
from src.middlewares.message_wrapping import LocalizedMessageWrapper
from src.schemas.video_schema import VideoCreate
from src.services.video_service import video_service
from src.use_cases.send_video_use_case import SendVideoUseCase
from src.yt_download.downloader import downloader

router = Router()
all_media_dir = 'res/yt-dir'


async def send_progress(message: Message):
    while (video_id := downloader.download_now_id.get(message.from_user.id)) == 'starting':
        await asyncio.sleep(1)

    percent = 0
    while video_id and (status := downloader.download_now[video_id]) != 'done':
        await asyncio.sleep(1)
        if percent != status:
            percent = status
            await message.edit_text(f'Процесс: {percent:.1f}%')


class DownloadingVideo(StatesGroup):
    download_in_progress = State()


@router.message(Command('start'))
async def start_message(_: Message, localized_message: LocalizedMessageWrapper):
    await localized_message.answer('start_message')


@router.message(StateFilter(None), UrlFilter())
async def get_link(message: Message, localized_message: LocalizedMessageWrapper):
    progress_message = await localized_message.answer('starting_download')

    # downloader.download_now_id[message.from_user.id] = 'starting'
    # tt = await asyncio.gather(send_progress(message), downloader.download(message.text, progress_message))
    result_video, video_id = await downloader.download(message.text, progress_message)
    await progress_message.delete()

    async with ChatActionSender.upload_video(message.from_user.id, message.bot):
        try:
            msg = await SendVideoUseCase().execute(result_video, message.answer_video)
        except BigFileError:
            await localized_message.answer('video_too_big')
            return
        except SendingError:
            await localized_message.answer('sending_error')
            return

    if not isinstance(result_video.file, str):
        video_file_id = msg.video.file_id

        await video_service.create(VideoCreate(id=video_id, file_id=video_file_id))

        os.remove(os.path.join(all_media_dir, result_video.cover + '.mp4'))
