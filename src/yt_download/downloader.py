import asyncio
from os import listdir

from aiogram.types import Message
from yt_dlp import YoutubeDL


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

    async def download(self, url: str, message: Message) -> tuple[str, dict]:
        video_info = get_video_info(url)
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
        return video_name, video_info


downloader = Downloader()
