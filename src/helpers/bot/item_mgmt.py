from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from bot import config
from bot.filters.callback_filters import item_cb
from bot.handlers.common.restart import reset_state
from bot.keyboards.employess.admin.admin_kb import itemManagerModel_admin, admin_panel_ADD_item_func, \
    admin_panel_UPDATE_item_func, admin_panel_DELETE_item_func
from bot.keyboards.employess.common.user_mgmt import post_user_mgmt_message_IK
from bot.keyboards.employess.manager.manager_kb import itemManagerModel_manager, manager_panel_ADD_item_func, \
    manager_panel_UPDATE_item_func, manager_panel_DELETE_item_func
from bot.states.ItemMgmtStates import ItemMgmtStates
from bot.strings.answer_blanks import items_mgmt_action_ADD_TEXT_pre, items_mgmt_action_DELETE_TEXT_pre, \
    items_mgmt_action_UPDATE_TEXT_pre, restart_command_TEXT_error
from helpers.bot.chat_mgmt import delete_previous_messages
from core import dispatcher, bot


def reg_item_handlers():
    dispatcher.register_callback_query_handler(items_handler, item_cb.filter())
    dispatcher.register_message_handler(add_item_hd, state=ItemMgmtStates.ADD)
    dispatcher.register_message_handler(update_item_hd, state=ItemMgmtStates.UPDATE)
    dispatcher.register_message_handler(delete_item_hd, state=ItemMgmtStates.DELETE)


@dispatcher.callback_query_handler(item_cb.filter())
async def items_handler(callback_query: types.CallbackQuery, callback_data: dict):
    await delete_previous_messages(tgtype=callback_query)
    action = callback_data.get('action')
    role = callback_data.get('role')
    text = str()
    if action == 'add':
        text = items_mgmt_action_ADD_TEXT_pre
        await ItemMgmtStates.ADD.set()
    elif action == 'update':
        text = items_mgmt_action_UPDATE_TEXT_pre
        await ItemMgmtStates.UPDATE.set()
    elif action == 'delete':
        text = items_mgmt_action_DELETE_TEXT_pre
        await ItemMgmtStates.DELETE.set()
    elif action == 'None':
        await post_user_mgmt_message_IK(callback_query.from_user.id, role)
    current_state = dispatcher.current_state(chat=callback_query.from_user.id, user=callback_query.from_user.id)
    if text:
        message = await bot.send_message(callback_query.from_user.id, text, parse_mode=types.ParseMode.MARKDOWN)
        await current_state.update_data({'items_management_msg_id': f"{message.message_id}", 'role': f"{role}"})


def item_mgmt_error_handler(func):
    async def inner_function(message: types.Message, state: FSMContext):
        try:
            data = await state.get_data()
            assert data['role'] is not None
            await func(message,  state)
        except KeyError as e:
            await state.finish()
            await reset_state(message, restart_command_TEXT_error)
            logger.error(f"add_item_hd: KeyError: {e.args}")

    return inner_function


@dispatcher.message_handler(state=ItemMgmtStates.ADD)
@item_mgmt_error_handler
async def add_item_hd(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.from_user.id in config.ADMINS:
        await itemManagerModel_admin.add_item(message, state, admin_panel_ADD_item_func, data['role'])
    elif message.from_user.id in config.MANAGERS:
        await itemManagerModel_manager.add_item(message, state, manager_panel_ADD_item_func, data['role'])


@dispatcher.message_handler(state=ItemMgmtStates.UPDATE)
@item_mgmt_error_handler
async def update_item_hd(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.from_user.id in config.ADMINS:
        await itemManagerModel_admin.update_item(message, state, admin_panel_UPDATE_item_func, data['role'])
    elif message.from_user.id in config.MANAGERS:
        await itemManagerModel_manager.update_item(message, state, manager_panel_UPDATE_item_func, data['role'])


@dispatcher.message_handler(state=ItemMgmtStates.DELETE)
@item_mgmt_error_handler
async def delete_item_hd(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.from_user.id in config.ADMINS:
        await itemManagerModel_admin.delete_item(message, state, admin_panel_DELETE_item_func, data['role'])
    elif message.from_user.id in config.MANAGERS:
        await itemManagerModel_manager.delete_item(message, state, manager_panel_DELETE_item_func, data['role'])
