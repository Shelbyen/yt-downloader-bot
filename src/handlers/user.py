import os
from urllib.error import URLError
from urllib.parse import urlparse

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile

from src.i18n.i18n import i18n
from src.yt_download.downloader import downloader

router = Router()
all_media_dir = 'res/yt-dir'


class DownloadingVideo(StatesGroup):
    download_in_progress = State()


@router.message(Command('start'))
async def start_message(message: Message):
    await message.answer(i18n.translate(message, 'start_message'))


@router.message(StateFilter(None))
async def get_link(message: Message):
    try:
        parsed_url = urlparse(message.text)
        hostname = parsed_url.hostname.split('.')
        if 'youtube' not in hostname and 'youtu' not in hostname:
            await message.answer(i18n.translate(message, 'wrong_link'))
            return
    except URLError:
        await message.answer(i18n.translate(message, 'wrong_link'))
        return

    file_name = downloader.download(message.text)
    video_file = FSInputFile(path=os.path.join(all_media_dir, file_name))
    await message.bot.send_video(message.from_user.id, video=video_file, caption=file_name[:-4])
