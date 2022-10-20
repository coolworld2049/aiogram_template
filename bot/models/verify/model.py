from typing import Any

from bot.models.role.role import UserRole
from bot.models.database.postgresql import asyncPostgresModel
from bot.models.database.postgresql.api import fetchone_user
from bot.utils.command_mgmt import manage_commands, ItemAction


class VerifyUser:
    __slots__ = (
        'commands',
        'common_commands',
        'admin_commands',
        'manager_commands',
        'admins',
        'employee_list',
        'managers',
        'values')

    def __init__(self, admins: set[int], managers: set[int], **kwargs: list[dict[str, str]]):
        """

        :param employee_list:
        :param kwargs: common_commands, admin_commands, manager_commands
        """
        employees = set()
        self.commands: list = []
        self.common_commands = kwargs.get('common_commands')
        self.admin_commands = kwargs.get('admin_commands')
        self.manager_commands = kwargs.get('manager_commands')
        self.admins = admins
        self.managers = managers
        self.employee_list = employees.union(self.admins, self.admins)
        self.values = None

    async def verify(self, user_id: int) -> dict[str, Any]:
        query = '''SELECT schema.upsert_table_user($1, $2)'''  # user_id, role
        if user_id and len(self.employee_list) > 0:
            is_admin = None
            is_manager = None
            if user_id in self.admins:
                self.commands = self.admin_commands
                self.values = [user_id, UserRole.ADMIN]
            elif user_id in self.managers:
                self.commands = self.manager_commands
                self.values = [user_id, UserRole.MANAGER]
            elif is_admin and is_manager:
                self.commands = self.manager_commands + self.admin_commands
            else:
                self.commands = self.common_commands
                self.values = [user_id, UserRole.USER]

            await manage_commands(action=ItemAction.SET, users_id=user_id, command_list=self.commands)
            await asyncPostgresModel.executeone(query, self.values)
            updated_user = await fetchone_user(user_id)
            return {'user_id': updated_user['user_id'], 'role': updated_user['role']}


