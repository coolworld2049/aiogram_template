from aiogram.dispatcher.filters import Command, CommandHelp, CommandStart

from bot.models.role.role import UserRole

command_start = CommandStart()
command_restart = Command('restart')
command_help = CommandHelp()
command_admin = Command(UserRole.ADMIN)
command_manager = Command(UserRole.MANAGER)
command_get_logs = Command('get_logs')
command_cancel = Command('cancel')
