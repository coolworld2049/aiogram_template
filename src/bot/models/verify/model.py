from typing import Any

from bot.models.database import asyncPostgresModel
from bot.models.role.role import UserRole
from bot.utils.bot_mgmt import set_bot_commands
from bot.utils.pgdbapi import fetchone_user


class VerifyUser:
    __slots__ = (
        'commands',
        'common_commands',
        'admin_commands',
        'manager_commands',
        'admins',
        'managers',
        'staff_list',
        'values')

    def __init__(self, staff_list: set[int], admins: set[int], managers: set[int], **kwargs: list[dict[str, str]]):
        """

        :param staff_list:
        :param kwargs: common_commands, admin_commands, manager_commands
        """
        self.commands: list = []
        self.common_commands = kwargs.get('common_commands')
        self.admin_commands = kwargs.get('admin_commands')
        self.manager_commands = kwargs.get('manager_commands')
        self.admins = admins
        self.managers = managers
        self.staff_list = staff_list
        self.values = None

    async def verify(self, user_id: int) -> dict[str, Any]:
        user = await fetchone_user(user_id)
        query = '''SELECT schema.upsert_table_user($1, $2)'''  # user_id, role
        if user and len(self.staff_list) > 0:
            for staff_user_id in self.staff_list:
                if staff_user_id in self.admins:
                    self.commands = self.admin_commands
                    self.values = [staff_user_id, UserRole.ADMIN]
                elif staff_user_id in self.managers:
                    self.commands = self.manager_commands
                    self.values = [staff_user_id, UserRole.MANAGER]
                if staff_user_id in self.admins and staff_user_id in self.managers:
                    self.commands = self.manager_commands + self.admin_commands
                elif staff_user_id not in self.staff_list:
                    self.commands = self.common_commands
                    self.values = [staff_user_id, UserRole.USER]

                await set_bot_commands(users_id=staff_user_id, command_list=self.commands)
                await asyncPostgresModel.executeone(query, self.values)
            updated_user = await fetchone_user(user_id)
            return {'user_id': updated_user['user_id'], 'role': updated_user['role']}
