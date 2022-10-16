from bot import config
from bot.config import admin_commands, manager_commands, common_commands, ADMINS, MANAGERS
from bot.models.database import asyncPostgresModel
from bot.utils.bot_mgmt import set_bot_commands
from bot.utils.pgdbapi import fetchone_user


class VerifyUser:
    __slots__ = ('commands', 'values')

    def __init__(self, commands: list[list[dict]]):
        """
        :param commands:
        """
        self.commands = commands
        self.values = None

    async def verify(self, user_id: int) -> dict[str, bool]:
        user = await fetchone_user(user_id)
        query = '''SELECT schema.upsert_table_user($1, $2, $3)'''  # user_id, is_admin, is_manager
        scope = ADMINS + MANAGERS
        if user and len(scope) > 0:
            for user_id in scope:
                check = (False, None)
                if user['is_admin'] in check or user_id in config.ADMINS:
                    self.commands = admin_commands
                    self.values = [user_id, True, True]
                elif user['is_manager'] in check or user_id in config.MANAGERS:
                    self.commands = manager_commands
                    self.values = [user_id, False, True]
                elif not user['is_admin'] and not user['is_manager']:
                    self.commands = common_commands
                    self.values = [user_id, False, False]

                await set_bot_commands(users_id=user_id, command_list=self.commands)
                await asyncPostgresModel.executeone(query, self.values)

                updated_user = await fetchone_user(user_id)
                return {'is_admin': updated_user['is_admin'], 'is_manager': updated_user['is_manager']}