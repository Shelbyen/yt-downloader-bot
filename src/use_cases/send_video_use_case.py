from aiogram.exceptions import TelegramBadRequest, TelegramEntityTooLarge

from src.exceptions.sending_exceptions import BigFileError, SendingError
from src.schemas.video_to_send_schema import VideoToSend


class SendVideoUseCase:
    async def execute(self, video: VideoToSend, send_function):
        try:
            msg = await send_function(**video.__dict__)
        except TelegramBadRequest as e:
            if 'FILE_PARTS_INVALID' in e.message:
                raise BigFileError() from e
            elif 'wrong type of the web page content' in e.message:
                video.cover = None
                msg = await send_function(**video.__dict__)
            else:
                raise SendingError() from e
        except TelegramEntityTooLarge as e:
            raise BigFileError() from e
        return msg
