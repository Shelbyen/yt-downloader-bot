from aiogram import F

from src.filters.permission_filter import PermissionFilter
from src.handlers import user, debug, group

debug.router.message.filter(PermissionFilter())
group.router.message.filter(F.chat.type in ["group", "supergroup"])


routers = (
    debug.router,
    user.router,
    group.router
)
