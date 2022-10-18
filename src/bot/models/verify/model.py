from typing import Any

from database import asyncPostgresModel
from bot.models.role.role import UserRole
from helpers.bot.command_mgmt import set_bot_commands
from database.postgresql.api import fetchone_user


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
        user = await fetchone_user(user_id)
        query = '''SELECT schema.upsert_table_user($1, $2)'''  # user_id, role
        if user and len(self.employee_list) > 0:
            for staff_user_id in self.employee_list:
                if staff_user_id in self.admins:
                    self.commands = self.admin_commands
                    self.values = [staff_user_id, UserRole.ADMIN]
                elif staff_user_id in self.managers:
                    self.commands = self.manager_commands
                    self.values = [staff_user_id, UserRole.MANAGER]
                if staff_user_id in self.admins and staff_user_id in self.managers:
                    self.commands = self.manager_commands + self.admin_commands
                elif staff_user_id not in self.employee_list:
                    self.commands = self.common_commands
                    self.values = [staff_user_id, UserRole.USER]

                await set_bot_commands(users_id=staff_user_id, command_list=self.commands)
                await asyncPostgresModel.executeone(query, self.values)
            updated_user = await fetchone_user(user_id)
            return {'user_id': updated_user['user_id'], 'role': updated_user['role']}
