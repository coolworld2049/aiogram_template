from bot.handlers.common.restart import reg_restart_handlers
from bot.handlers.staff.admin_hd import reg_admin_handlers
from bot.handlers.common.get_logs import reg_get_logs_handler
from bot.handlers.common.help import reg_help_handler
from bot.handlers.common.start import reg_start_handlers
from bot.handlers.helpers.item_hd import reg_item_handlers
from bot.handlers.staff.manager_hd import reg_manager_handlers
from bot.handlers.user.common.common_hd import reg_common_handlers
from bot.handlers.user.contractor.contractor_hd import reg_customer_handlers
from bot.handlers.user.customer.customer_hd import reg_contractor_handlers
from bot.utils.pagination import reg_pagination_handlers


def setup_handlers():
    reg_start_handlers()
    reg_restart_handlers()
    reg_help_handler()
    reg_get_logs_handler()
    reg_common_handlers()
    reg_admin_handlers()
    reg_manager_handlers()
    reg_contractor_handlers()
    reg_customer_handlers()
    reg_item_handlers()
    reg_pagination_handlers()
