from bot import config
from bot.models.verify.model import VerifyUser
from strings.commands import common_commands, manager_commands, admin_commands

verifyUserModel = VerifyUser(admins=config.ADMINS, managers=config.MANAGERS,
                             common_commands=common_commands, admin_commands=admin_commands,
                             manager_commands=manager_commands)
