from bot.commands.reload import reg_restart_handlers
from bot.handlers.admin.admin_hd import reg_admin_handlers
from bot.commands.get_logs import reg_get_logs_handler
from bot.commands.help import reg_help_handler
from bot.commands.start import reg_start_handlers
from bot.handlers.user.common_hd import reg_common_handlers
from bot.utils.pagination import reg_pagination_handlers


def setup_handlers():
    reg_start_handlers()
    reg_restart_handlers()
    reg_help_handler()
    reg_get_logs_handler()
    reg_common_handlers()
    reg_admin_handlers()
    reg_pagination_handlers()
