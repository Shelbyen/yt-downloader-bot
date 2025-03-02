def create_info_dict_for_send(video_info: dict) -> dict:
    return {'width': video_info['width'],
            'height': video_info['height'],
            'duration': video_info['duration'],
            'cover': video_info['thumbnail'],
            'caption': video_info['title'] + f' [{video_info["id"]}]',
            'supports_streaming': True
            }
