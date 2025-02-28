from urllib.error import URLError
from urllib.parse import urlparse

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from src.i18n.i18n import i18n
from src.yt_download.downloader import downloader

router = Router()


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
        print(hostname)
        if 'youtube' not in hostname and 'youtu' not in hostname:
            await message.answer(i18n.translate(message, 'wrong_link'))
            return
    except URLError:
        await message.answer(i18n.translate(message, 'wrong_link'))
        return

    file_name = downloader.download(parsed_url)

    await message.bot.send_video(message.from_user.id, video=file_name, caption=file_name[:-4])
