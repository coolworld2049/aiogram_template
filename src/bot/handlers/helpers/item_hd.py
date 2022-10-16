from aiogram import types

from bot.answer_blanks.lang import items_mgmt_action_ADD_TEXT_pre, items_mgmt_action_DELETE_TEXT_pre, \
    items_mgmt_action_UPDATE_TEXT_pre
from bot.filters.callback_filters import item_cb
from bot.filters.command_filters import command_admin
from bot.keyboards.staff.admin_kb import user_mgmt_message_IK
from bot.states.ItemMgmtStates import ItemMgmtStates
from bot.utils.chat_mgmt import delete_previous_messages
from core import dispatcher, bot


def reg_item_handlers():
    dispatcher.register_callback_query_handler(items_handler, item_cb.filter())


@dispatcher.callback_query_handler(item_cb.filter())
async def items_handler(callback_query: types.CallbackQuery, callback_data: dict):
    await delete_previous_messages(tgtype=callback_query)
    action = callback_data.get('action')
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
        callback = callback_data.get('callback')
        if callback == command_admin.commands[0]:
            await user_mgmt_message_IK(callback_query.from_user.id)
    if text:
        message = await bot.send_message(callback_query.from_user.id, text,
                                         parse_mode=types.ParseMode.MARKDOWN)
        await dispatcher.current_state(chat=callback_query.from_user.id,
                                       user=callback_query.from_user.id) \
            .update_data({'items_management_msg_id': f"{message.message_id}"})
