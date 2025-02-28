from os import listdir

from yt_dlp import YoutubeDL


def progress_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')


ydl_opts = {
    'format': 'bv[width<=1920][ext=mp4]+ba[ext=m4a]',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio'
    }],
    'merge_output_format': 'mp4',
    'socket_timeout': 60,
    'progress_hooks': [progress_hook]
}


class Downloader:
    def __init__(self):
        self.ydl = YoutubeDL(ydl_opts)


    def check_video_info(self, url):
        info = self.ydl.extract_info(url, download=False)
        duration = info.get('duration')
        if duration and duration > 4 * 60 * 60:
            raise Exception('The video is too long')
        return info.get('id')

    def download(self, url) -> str:
        video_id = self.check_video_info(url)
        print(video_id)
        error_code = self.ydl.download(url)
        if error_code:
            raise Exception('Video failed to download')

        for file_name in listdir():
            if file_name.endswith(f'[{video_id}].mp4'):
                return file_name


downloader = Downloader()
