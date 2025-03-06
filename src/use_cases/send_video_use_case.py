from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from src.exceptions.sending_exceptions import BigFileError, SendingError
from src.schemas.video_to_send_schema import VideoToSend


class SendVideoUseCase:
    async def execute_answer(self, video: VideoToSend, user_message: Message):
        try:
            msg = await user_message.answer_video(**video.__dict__)
        except TelegramBadRequest as e:
            if 'FILE_PARTS_INVALID' in e.message:
                raise BigFileError()
            elif 'wrong type of the web page content' in e.message:
                video.cover = None
                msg = await user_message.answer_video(**video.__dict__)
            else:
                raise SendingError()
        return msg

    async def execute_reply(self, video: VideoToSend, user_message: Message):
        try:
            msg = await user_message.reply_video(**video.__dict__)
        except TelegramBadRequest as e:
            if 'FILE_PARTS_INVALID' in e.message:
                raise BigFileError()
            elif 'wrong type of the web page content' in e.message:
                video.cover = None
                msg = await user_message.reply_video(**video.__dict__)
            else:
                raise SendingError()
        return msg
