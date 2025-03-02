from aiogram import Router, F
from aiogram.types import Message

from src.filters.url_filter import UrlFilter
from src.i18n.i18n import i18n
from src.yt_download.downloader import downloader

router = Router()

@router.message(UrlFilter())
async def check_message(message: Message):
    progress_message = await message.answer(i18n.translate(message, 'starting_download'))
    result_info = await downloader.download(message.text, progress_message)

    # if result_info[2]:
    #     await extract_info_send_video(progress_message, result_info[0], result_info[1])
    #     return
    # if not (result_info[0] and result_info[1]):
    #     await message.answer(i18n.translate(message, 'wrong_link'))
    #     return
    # video_name, info, _ = result_info
    #
    # async with ChatActionSender.upload_video(message.from_user.id, message.bot):
    #     video_file = FSInputFile(path=os.path.join(all_media_dir, video_name))
    #     msg = await extract_info_send_video(progress_message, video_file, info)
    # video_file_id = msg.video.file_id
    # await video_service.create(VideoCreate(id=info['id'], file_id=video_file_id))
    #
    # os.remove(os.path.join(all_media_dir, video_name))

