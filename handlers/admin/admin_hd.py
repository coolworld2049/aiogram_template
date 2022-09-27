import asyncio

from aiogram import types

from config import MESSAGE_DELAY, admin_commands
from core import dp, is_admin, set_my_commands
from keyboards.admin.admin_kb import items_management_message_IK, admin_panel_message_IK


def reg_admin_handlers():
    dp.register_message_handler(admin, commands=['admin'])
    dp.register_callback_query_handler(items_management, lambda c: c.data == "items-management")


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if await is_admin(message.from_user.id):
        await set_my_commands(users_id=message.from_user.id, command_list=admin_commands)
        await admin_panel_message_IK(message.from_user.id)


@dp.callback_query_handler(lambda c: c.data == "items-management")
async def items_management(callback_query: types.CallbackQuery):
    await items_management_message_IK(callback_query.from_user.id)
    await callback_query.message.delete()
    await asyncio.sleep(MESSAGE_DELAY)
