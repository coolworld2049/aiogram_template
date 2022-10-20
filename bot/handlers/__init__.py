from bot.handlers.common.reload import reg_restart_handlers
from bot.handlers.common.get_logs import reg_get_logs_handler
from bot.handlers.common.help import reg_help_handler
from bot.handlers.common.start import reg_start_handlers
from bot.handlers.user.common.common_hd import reg_common_handlers
from bot.handlers.user.contractor.contractor_hd import reg_customer_handlers
from bot.handlers.user.customer.customer_hd import reg_contractor_handlers


def setup_handlers():
    reg_start_handlers()
    reg_restart_handlers()
    reg_help_handler()
    reg_get_logs_handler()
    reg_common_handlers()
    reg_contractor_handlers()
    reg_customer_handlers()
