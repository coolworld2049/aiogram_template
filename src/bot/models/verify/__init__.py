from bot import config
from bot.config import common_commands, admin_commands, manager_commands
from bot.models.verify.model import VerifyUser

verifyUserModel = VerifyUser(admins=config.ADMINS, managers=config.MANAGERS,
                             common_commands=common_commands, admin_commands=admin_commands,
                             manager_commands=manager_commands)
