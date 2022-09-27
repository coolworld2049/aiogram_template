import asyncio

from aiogram import types

from config import MESSAGE_DELAY, DEMO_MODE
from core import dp, bot
from keyboards.user.common.common_inline_kb import get_number_active_orders
from keyboards.user.order.common_order_kb import order_CONFIRM_message_IK, set_order_EXECUTOR_message_IK
from states.OrderStates import OrderStates
from utils.chat_mgmt import delete_message


def reg_common_order_handlers():
    dp.register_callback_query_handler(order_execute, lambda c: str(c.data).split('_')[1] == "order-execute", state='*')
    dp.register_callback_query_handler(confirm_order_publication_yes,
                                       lambda c: str(c.data).split('_')[1] == "publication-order-yes", state='*')
    dp.register_callback_query_handler(confirm_order_publication_no,
                                       lambda c: str(c.data).split('_')[1] == "create-order-no", state='*')


@dp.callback_query_handler(lambda c: str(c.data).split('_')[1] == "order-execute", state='*')
async def order_execute(callback_query: types.CallbackQuery):
    if not DEMO_MODE:
        has_active_orders = await get_number_active_orders(callback_query.from_user.id, 'contractor', as_traveler=True)
        if has_active_orders:
            order_id = int(callback_query.data.split('_')[0])
            msg_ids = callback_query.data.split('_')[-1]
            if msg_ids:
                await asyncio.sleep(MESSAGE_DELAY)
                await callback_query.message.delete()
                await delete_message(callback_query.from_user.id, msg_ids, MESSAGE_DELAY)
            else:
                await asyncio.sleep(MESSAGE_DELAY)
                await callback_query.message.delete()
            await set_order_EXECUTOR_message_IK(callback_query.from_user.id, order_id)
    else:
        await bot.send_message(callback_query.from_user.id, 'Вы не можете сделать это действие в демонстрационном режиме')


@dp.callback_query_handler(lambda c: str(c.data).split('_')[1] == "publication-order-yes", state='*')
async def confirm_order_publication_yes(callback_query: types.CallbackQuery):
    spl = callback_query.data.split('_')
    order_id = int(spl[0])
    role = spl[-1]
    await order_CONFIRM_message_IK(callback_query.from_user.id, order_id, role, OrderStates.order_accepted.state)


@dp.callback_query_handler(lambda c: str(c.data).split('_')[1] == "publication-order-no", state='*')
async def confirm_order_publication_no(callback_query: types.CallbackQuery):
    spl = callback_query.data.split('_')
    order_id = int(spl[0])
    role = spl[-1]
    await order_CONFIRM_message_IK(callback_query.from_user.id, order_id, role, OrderStates.order_terminated.state)
