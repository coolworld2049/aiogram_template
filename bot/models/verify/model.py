from typing import Any

from bot import config
from bot.commands.commands_config import common_commands, admin_commands
from bot.models.database.postgresql.api import fetchone_user
from bot.models.database.postgresql.model import asyncPostgresModel
from bot.models.role.role import UserRole
from bot.utils.command_mgmt import manage_commands, ItemAction


class VerifyUser:
    __slots__ = (
        'commands',
        'common_commands',
        'admin_commands',
        'white_list',
        'values')

    def __init__(self, white_list: set[int], **kwargs: list[dict[str, str]]):
        """

        :param employee_list:
        :param kwargs: common_commands, admin_commands, manager_commands
        """
        self.commands: list = []
        self.common_commands = kwargs.get('common_commands')
        self.admin_commands = kwargs.get('admin_commands')
        self.white_list = white_list
        self.values = None

    async def verify(self, user_id: int) -> dict[str, Any]:
        query = '''SELECT schema.upsert_table_user($1, $2)'''  # user_id, role
        if user_id in self.white_list:
            self.commands = self.admin_commands
            self.values = [user_id, UserRole.ADMIN]
        else:
            self.commands = self.common_commands
            self.values = [user_id, UserRole.USER]

        await manage_commands(action=ItemAction.SET, users_id=user_id, command_list=self.commands)
        await asyncPostgresModel.executeone(query, self.values)
        updated_user = await fetchone_user(user_id)
        return {'user_id': updated_user['user_id'], 'role': updated_user['role']}


verifyUserModel = VerifyUser(white_list=config.ADMINS, common_commands=common_commands, admin_commands=admin_commands)
