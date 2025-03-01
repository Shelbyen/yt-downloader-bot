from os import listdir

from yt_dlp import YoutubeDL


def progress_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')


def shorted_than_a_time(info, *, incomplete):
    duration = info.get('duration')
    if duration and duration > 4 * 60 * 60:
        return 'The video is too long'


ydl_opts = {
    'format': 'bv[width<=1920][ext=mp4]+ba[ext=m4a]',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio'
    }],
    'merge_output_format': 'mp4',
    'socket_timeout': 60,
    'progress_hooks': [progress_hook],
    'match_filter': shorted_than_a_time,
    'paths': {'home': 'res/yt-dir', 'temp': 'temp'},
    'quiet': True
}


def get_video_id(url) -> str:
    with YoutubeDL({'check_formats': False, 'quiet': True}) as ytl:
        info = ytl.extract_info(url, download=False)
    return info.get('id')


class Downloader:
    def __init__(self):
        self.ydl = YoutubeDL(ydl_opts)

    def download(self, url: str) -> str:
        video_id = get_video_id(url)
        error_code = self.ydl.download(url)
        if error_code:
            raise Exception('Video failed to download')

        for file_name in listdir('res/yt-dir'):
            if file_name.endswith(f'[{video_id}].mp4'):
                return file_name


downloader = Downloader()
