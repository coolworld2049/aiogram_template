from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from bot.models.role.role import UserRole


class RoleMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, admins: list, managers: list):
        super().__init__()
        self.admins = admins
        self.managers = managers

    async def pre_process(self, obj, data, *args):
        if not getattr(obj, "from_user", None):
            data["role"] = None
        elif obj.from_user.id in self.admins:
            data["role"] = UserRole.ADMIN
        elif obj.from_user.id in self.managers\
                and obj.from_user.id not in self.admins:
            data["role"] = UserRole.MANAGER
        else:
            data["role"] = UserRole.USER

    async def post_process(self, obj, data, *args):
        del data["role"]
