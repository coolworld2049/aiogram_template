from bot import config
from bot.config import common_commands, admin_commands, manager_commands
from bot.models.verify.model import VerifyUser

staff_list = config.ADMINS
staff_list.union(config.MANAGERS)
verifyUserModel = VerifyUser(staff_list=staff_list,
                             admins=config.ADMINS,
                             managers=config.MANAGERS,
                             common_commands=common_commands,
                             admin_commands=admin_commands,
                             manager_commands=manager_commands)
