from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from src.config.project_config import settings


class PermissionFilter(BaseFilter):
    def __init__(self, is_exists: bool = True) -> None:
        self.is_exists = is_exists

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user = str(event.from_user.id) in settings.ADMINS.split('/')
        return user == self.is_exists
