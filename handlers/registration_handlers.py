from handlers.commands.get_logs import reg_get_logs_handler
from handlers.commands.help import reg_help_handler
from handlers.commands.start import reg_start_handlers
from handlers.user.common.common_hd import reg_common_interface_handlers
from handlers.user.customer.customer_hd import reg_contractor_handlers
from handlers.user.contractor.contractor_hd import reg_customer_handlers
from handlers.user.order.common_order_hd import reg_common_order_handlers
from handlers.user.order.contractor_order_hd import reg_contractor_order_handlers
from handlers.user.order.customer_order_hd import reg_customer_order_handlers
from utils.pagination import reg_pagination_handlers


def registrate_all_handlers():
    reg_start_handlers()
    reg_common_interface_handlers()
    reg_contractor_handlers()
    reg_customer_handlers()
    reg_contractor_order_handlers()
    reg_customer_order_handlers()
    reg_get_logs_handler()
    reg_common_order_handlers()
    reg_pagination_handlers()
    reg_help_handler()
