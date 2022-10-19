from bot import config
from strings.locale import common_commands, admin_commands, manager_commands
from bot.models.verify.model import VerifyUser

verifyUserModel = VerifyUser(admins=config.ADMINS, managers=config.MANAGERS,
                             common_commands=common_commands, admin_commands=admin_commands,
                             manager_commands=manager_commands)
