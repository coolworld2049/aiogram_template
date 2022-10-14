from handlers.commands.get_logs import reg_get_logs_handler
from handlers.commands.help import reg_help_handler
from handlers.commands.start import reg_start_handlers
from handlers.user.common.common_hd import reg_common_handlers
from handlers.user.contractor.contractor_hd import reg_customer_handlers
from handlers.user.customer.customer_hd import reg_contractor_handlers
from utils.pagination import reg_pagination_handlers


def setup_handlers():
    reg_start_handlers()
    reg_help_handler()
    reg_get_logs_handler()
    reg_common_handlers()
    reg_contractor_handlers()
    reg_customer_handlers()
    reg_pagination_handlers()
