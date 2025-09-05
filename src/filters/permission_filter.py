from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from src.config import project_settings


class PermissionFilter(BaseFilter):
    """ On ADMINS list or not """
    def __init__(self, is_exists: bool = True) -> None:
        self.is_exists = is_exists

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        if event.from_user is None:
            return False
        user = str(event.from_user.id) in project_settings.ADMINS.split('/')
        return user == self.is_exists
