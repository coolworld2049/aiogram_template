from aiogram import types
from aiogram.dispatcher import FSMContext

from config import admin_commands
from core import dp, bot
from data.database.db_api import is_admin
from keyboards.admin.admin_kb import admin_items_management_message_IK, admin_panel_message_IK, \
    admin_add_item_controller, admin_delete_item_controller, admin_update_item_controller
from states.AdminStates import AdminStates
from utils.bot_mgmt import set_my_commands
from utils.chat_mgmt import delete_previous_messages


def reg_admin_handlers():
    dp.register_message_handler(admin, commands=['admin'])
    dp.register_callback_query_handler(admin_items_management,
                                       lambda c: str(c.data).split('_')[1] == "admin-items-management")
    dp.register_message_handler(admin_add_item, state=AdminStates.add_item)
    dp.register_message_handler(admin_update_item, state=AdminStates.update_item)
    dp.register_message_handler(admin_delete_item, state=AdminStates.delete_item)


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if await is_admin(message.from_user.id):
        await set_my_commands(users_id=message.from_user.id, command_list=admin_commands)
        await admin_panel_message_IK(message.from_user.id)


@dp.callback_query_handler(lambda c: str(c.data).split('_')[1] == "admin-items-management")
async def admin_items_management(callback_query: types.CallbackQuery):
    await delete_previous_messages(tgtype=callback_query)
    spl = callback_query.data.split('_')
    if len(spl) == 3 or len(spl) == 4:
        action = spl[2]
        if action == 'add':
            await bot.send_message(callback_query.from_user.id, 'текст 1. Отменить добавление: /cancel')
            await AdminStates.add_item.set()
        if action == 'update':
            await bot.send_message(callback_query.from_user.id, 'текст 2. Отменить добавление: /cancel')
            await AdminStates.update_item.set()
        elif action == 'delete':
            await bot.send_message(callback_query.from_user.id, 'текст 3. Отменить добавление: /cancel')
            await AdminStates.delete_item.set()
    else:
        await admin_items_management_message_IK(callback_query.from_user.id)


@dp.message_handler(state=AdminStates.add_item)
async def admin_add_item(message: types.Message, state: FSMContext):
    await delete_previous_messages(tgtype=message)
    await admin_add_item_controller(message, state)


@dp.message_handler(state=AdminStates.update_item)
async def admin_update_item(message: types.Message, state: FSMContext):
    await delete_previous_messages(tgtype=message)
    await admin_update_item_controller(message, state)


@dp.message_handler(state=AdminStates.delete_item)
async def admin_delete_item(message: types.Message, state: FSMContext):
    await delete_previous_messages(tgtype=message)
    await admin_delete_item_controller(message, state)
