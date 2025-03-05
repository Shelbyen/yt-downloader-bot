from src.filters.chat_type_filter import ChatTypeFilter
from src.filters.permission_filter import PermissionFilter
from src.handlers import user, debug, group
from src.middlewares.message_wrapping import MessageWrappingMiddleware

user.router.message.outer_middleware(MessageWrappingMiddleware())
group.router.message.outer_middleware(MessageWrappingMiddleware())

debug.router.message.filter(PermissionFilter())
user.router.message.filter(ChatTypeFilter(is_group=False))
group.router.message.filter(ChatTypeFilter(is_group=True))

routers = (
    debug.router,
    user.router,
    group.router
)
