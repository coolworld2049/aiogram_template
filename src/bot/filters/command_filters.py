from aiogram.dispatcher.filters import Command, CommandHelp, CommandStart

command_start = CommandStart()
command_help = CommandHelp()
command_admin = Command('admin')
command_get_logs = Command('get_logs')

command_cancel = Command('cancel')
