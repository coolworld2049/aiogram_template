from aiogram import types
from aiogram.dispatcher import FSMContext

from config import admin_commands
from core import dp, bot
from data.database.db_api import user_is_admin
from filters.callback_filters import admin_cb
from keyboards.admin.admin_kb import admin_items_management_message_IK, admin_panel_message_IK, \
    admin_add_item_controller, admin_delete_item_controller, admin_update_item_controller
from states.AdminStates import AdminStates
from utils.bot_mgmt import set_my_commands
from utils.chat_mgmt import delete_previous_messages


def reg_admin_handlers():
    dp.register_message_handler(admin, commands=['admin'])
    dp.register_callback_query_handler(admin_items_management, admin_cb.filter())
    dp.register_message_handler(admin_add_item, state=AdminStates.add_item)
    dp.register_message_handler(admin_update_item, state=AdminStates.update_item)
    dp.register_message_handler(admin_delete_item, state=AdminStates.delete_item)


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if await user_is_admin(message.from_user.id):
        await set_my_commands(users_id=message.from_user.id, command_list=admin_commands)
        await admin_panel_message_IK(message.from_user.id)


@dp.callback_query_handler(admin_cb.filter())
async def admin_items_management(callback_query: types.CallbackQuery, callback_data: dict):
    await delete_previous_messages(tgtype=callback_query)
    action = callback_data.get('action')
    if action == 'add':
        await bot.send_message(callback_query.from_user.id, 'текст 1. Отменить добавление: /cancel')
        await AdminStates.add_item.set()
    elif action == 'update':
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
