import os

from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.utils.chat_action import ChatActionSender

from src.filters.url_filter import UrlFilter
from src.i18n.i18n import i18n
from src.schemas.video_schema import VideoCreate
from src.services.video_service import video_service
from src.use_cases.download_send_video_use_case import create_info_dict_for_send
from src.yt_download.downloader import downloader

router = Router()
all_media_dir = 'res/yt-dir'


@router.message(UrlFilter(answer_when_wrong=False))
async def check_message(message: Message):
    progress_message = await message.reply(i18n.translate(message, 'starting_download'))

    result_info = await downloader.download(message.text, progress_message)

    await progress_message.delete()

    if not (result_info[0] and result_info[1]):
        return

    video_name, info, is_exist = result_info

    if is_exist:
        await message.reply_video(video_name, **create_info_dict_for_send(info))
        return

    async with ChatActionSender.upload_video(message.from_user.id, message.bot):
        video_file = FSInputFile(path=os.path.join(all_media_dir, video_name))
        msg = await message.reply_video(video_file, **create_info_dict_for_send(info))

    video_file_id = msg.video.file_id
    await video_service.create(VideoCreate(id=info['id'], file_id=video_file_id))

    os.remove(os.path.join(all_media_dir, video_name))
