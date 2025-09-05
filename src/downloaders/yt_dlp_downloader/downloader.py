import os
from os import listdir

from aiogram.types import FSInputFile
from yt_dlp import YoutubeDL

from src.downloaders.downloader import Downloader
from src.schemas.video_schema import VideoBase
from src.schemas.video_to_send_schema import VideoToSend
from src.services.video_service import video_service


def progress_hook(d):
    pass


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
    'quiet': True,
    'cookiefile': 'res/yt-dir/cookies/shebik_cookies.txt'
}


def get_video_info(url) -> dict:
    with YoutubeDL({'check_formats': False, 'quiet': True, 'cookiefile': 'res/yt-dir/cookies/shebik_cookies.txt'}) as ytl:
        info = ytl.extract_info(url, download=False)
    return info


class YtDlpDownloader(Downloader):
    def __init__(self):
        self.download_now = {}
        self.download_now_id = {}

    async def download(self, url: str, *args, **kwargs) -> tuple[VideoToSend, str]:
        video_info = get_video_info(url)

        saved_file_id: VideoBase | None = await video_service.get(video_info['id'])
        if saved_file_id:
            return (VideoToSend(video=saved_file_id.file_id,
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
        return (VideoToSend(video=FSInputFile(path=os.path.join('res/yt-dir', video_name)),
                            caption=video_name[:-4],
                            width=video_info.get('width'),
                            height=video_info.get('height'),
                            duration=video_info.get('duration'),
                            cover=video_info.get('thumbnail')
                            ),
                video_info['id'])
