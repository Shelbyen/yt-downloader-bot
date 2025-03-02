from src.filters.chat_type_filter import ChatTypeFilter
from src.filters.permission_filter import PermissionFilter
from src.handlers import user, debug, group

debug.router.message.filter(PermissionFilter())
user.router.message.filter(ChatTypeFilter(is_group=False))
group.router.message.filter(ChatTypeFilter(is_group=True))

routers = (
    debug.router,
    user.router,
    group.router
)
