import asyncio
import os
from urllib.error import URLError
from urllib.parse import urlparse

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile, InputFile
from aiogram.utils.chat_action import ChatActionSender

from src.i18n.i18n import i18n
from src.schemas.video_schema import VideoCreate
from src.services.video_service import video_service
from src.yt_download.downloader import downloader

router = Router()
all_media_dir = 'res/yt-dir'


async def extract_info_send_video(message: Message, video_file: InputFile | str, yt_info: dict):
    msg = await message.answer_video(video_file,
                                     width=yt_info['width'],
                                     height=yt_info['height'],
                                     duration=yt_info['duration'],
                                     cover=yt_info['thumbnail'],
                                     caption=yt_info['title'] + f' [{yt_info["id"]}]',
                                     supports_streaming=True)
    return msg


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
async def start_message(message: Message):
    await message.answer(i18n.translate(message, 'start_message'))


@router.message(StateFilter(None), F.text)
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

    progress_message = await message.answer(i18n.translate(message, 'starting_download'))

    # downloader.download_now_id[message.from_user.id] = 'starting'
    # tt = await asyncio.gather(send_progress(message), downloader.download(message.text, progress_message))
    result_info = await downloader.download(message.text, progress_message)

    if result_info[2]:
        await extract_info_send_video(progress_message, result_info[0], result_info[1])
        return
    if not (result_info[0] and result_info[1]):
        await message.answer(i18n.translate(message, 'wrong_link'))
        return
    video_name, info, _ = result_info

    async with ChatActionSender.upload_video(message.from_user.id, message.bot):
        video_file = FSInputFile(path=os.path.join(all_media_dir, video_name))
        msg = await extract_info_send_video(progress_message, video_file, info)
    video_file_id = msg.video.file_id
    await video_service.create(VideoCreate(id=info['id'], file_id=video_file_id))

    os.remove(os.path.join(all_media_dir, video_name))
