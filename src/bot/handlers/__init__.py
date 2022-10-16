from bot.handlers.admin.admin_hd import reg_admin_handlers
from bot.handlers.common.commands.get_logs import reg_get_logs_handler
from bot.handlers.common.commands.help import reg_help_handler
from bot.handlers.common.commands.start import reg_start_handlers
from bot.handlers.item.item_hd import reg_item_handlers
from bot.handlers.user.common.common_hd import reg_common_handlers
from bot.handlers.user.contractor.contractor_hd import reg_customer_handlers
from bot.handlers.user.customer.customer_hd import reg_contractor_handlers
from bot.utils.pagination import reg_pagination_handlers


def setup_handlers():
    reg_start_handlers()
    reg_help_handler()
    reg_get_logs_handler()
    reg_common_handlers()
    reg_admin_handlers()
    reg_contractor_handlers()
    reg_customer_handlers()
    reg_item_handlers()
    reg_pagination_handlers()
