from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message(F.video)
async def set_video(message: Message, state: FSMContext):
    video_id = message.video.file_id
    await state.set_data({'video': video_id})
    await message.answer('Прочитал!')


@router.message(Command('get_video'))
async def get_video(message: Message, state: FSMContext):
    video_id = await state.get_value('video')
    await message.answer_video(video=video_id)
