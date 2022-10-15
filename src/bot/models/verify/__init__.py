from bot.config import common_commands, admin_commands, manager_commands
from bot.models.verify.model import VerifyUser

verifyUserModel = VerifyUser([common_commands, admin_commands, manager_commands])
