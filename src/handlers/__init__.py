from src.filters.permission_filter import PermissionFilter
from src.handlers import user, debug

debug.router.message.filter(PermissionFilter())

routers = (
    user.router,
    debug.router
)
