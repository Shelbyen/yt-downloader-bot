import asyncio
import os
from os import listdir

from aiogram.types import Message, FSInputFile
from yt_dlp import YoutubeDL

from src.schemas.video_schema import VideoBase
from src.schemas.video_to_send_schema import VideoToSend
from src.services.video_service import video_service


def progress_hook(d):
    if d['status'] == 'downloading' and d.get('total_bytes_estimate') and d.get('downloaded_bytes'):
        pr = d['downloaded_bytes'] / d['total_bytes_estimate']
        downloader.download_now[d['info_dict']['id']] = pr
    else:
        downloader.download_now[d['info_dict']['id']] = 'done'
    asyncio.get_event_loop().create_task(asyncio.sleep(0.01))


def shorted_than_a_time(info, *, incomplete):
    duration = info.get('duration')
    if duration and duration > 4 * 60 * 60:
        return 'The video is too long'


ydl_opts = {
    'format': 'bv[width<=1920][ext=mp4]+ba[ext=m4a]',
    'merge_output_format': 'mp4',
    'socket_timeout': 60,
    # 'progress_hooks': [progress_hook],
    'match_filter': shorted_than_a_time,
    'paths': {'home': 'res/yt-dir', 'temp': 'temp'},
    'quiet': True
}


def get_video_info(url) -> dict:
    with YoutubeDL({'check_formats': False, 'quiet': True}) as ytl:
        info = ytl.extract_info(url, download=False)
    return info


class Downloader:
    def __init__(self):
        self.download_now = {}
        self.download_now_id = {}

    async def download(self, url: str, message: Message) -> tuple[VideoToSend, str] | None:
        video_info = get_video_info(url)

        saved_file_id: VideoBase | None = await video_service.get(video_info['id'])
        if saved_file_id:
            return (VideoToSend(file=saved_file_id.file_id,
                                caption=video_info['title'] + f' [{video_info["id"]}]',
                                width=video_info.get('width'),
                                height=video_info.get('height'),
                                duration=video_info.get('duration'),
                                cover=video_info.get('thumbnail')
                                ),
                    video_info['id'])

        # self.download_now_id[message.from_user.id] = video_id
        # self.download_now[video_id] = 0

        ydl = YoutubeDL(ydl_opts)

        error_code = ydl.download(url)
        if error_code:
            raise Exception('Video failed to download')

        video_name = None
        for file_name in listdir('res/yt-dir'):
            if file_name.endswith(f'[{video_info["id"]}].mp4'):
                video_name = file_name
        return (VideoToSend(file=FSInputFile(path=os.path.join('res/yt-dir', video_name)),
                            caption=video_name[:-4],
                            width=video_info.get('width'),
                            height=video_info.get('height'),
                            duration=video_info.get('duration'),
                            cover=video_info.get('thumbnail')
                            ),
                video_info['id'])


downloader = Downloader()
