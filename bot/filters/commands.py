from aiogram.dispatcher.filters import Command, CommandHelp, CommandStart

from bot.models.role.role import UserRole

command_start = CommandStart()
command_reload = Command('reload')
command_help = CommandHelp()
command_admin = Command(UserRole.ADMIN)
command_manager = Command(UserRole.MANAGER)
command_logs = Command('logs')
command_cancel = Command('cancel')
