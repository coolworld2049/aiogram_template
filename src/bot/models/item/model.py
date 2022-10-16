import typing

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.answer_blanks.lang import user_state_incorrect_input_TEXT
from bot.filters.command_filters import command_cancel
from bot.utils.chat_mgmt import delete_previous_messages


class ItemManagerModel:
    __slots__ = ('pre_proccess_func', 'post_proccess_func')

    def __init__(self, pre_proccess_func, post_proccess_func):
        """
        async def pre_proccess_func(user_id: int):
            await delete_previous_messages(user_id)
            IK = types.InlineKeyboardMarkup() \
                .add(types.InlineKeyboardButton(admin_panel_BTN_TEXT,
                                                callback_data=admin_cb.new(action='None')))
            message = await bot.send_message(user_id, admin_panel_TEXT, reply_markup=IK)
            await save_message(user_id, message.message_id)

        async def post_proccess_func(user_id: int):
            await delete_previous_messages(user_id)
            IK = types.InlineKeyboardMarkup(row_width=2)
            items = ['item 1', 'item 2', 'item 3', 'item 4']
            if items and len(items) > 0:
                for item in items:
                    item_text = f"{item}"
                    IK.insert(types.InlineKeyboardButton(item_text, callback_data=admin_cb.new(action='update')))
                IK.row(types.InlineKeyboardButton('➕', callback_data=admin_cb.new(action='add')),
                       types.InlineKeyboardButton('➖', callback_data=admin_cb.new(action='delete')))
                IK.row(types.InlineKeyboardButton(navigation_BTN_back,
                                                  callback_data=back_cb.new(to='admin-panel', msg_ids='None')))
                IK.row(types.InlineKeyboardButton(navigation_BTN_back_to_menu,
                                                  callback_data=back_cb.new(to='menu', msg_ids='None')))
                message = await bot.send_message(user_id, admin_items_mgmt_message_IK_TEXT,
                                                 reply_markup=IK, parse_mode=types.ParseMode.MARKDOWN)
                await save_message(user_id, message.message_id)
            else:
                message = await bot.send_message(user_id, admin_items_mgmt_message_IK_TEXT_error,
                                                 reply_markup=IK)
                await save_message(user_id, message.message_id)
        """
        self.pre_proccess_func = pre_proccess_func
        self.post_proccess_func = post_proccess_func

    async def __state_handler(self, message: types.Message, state: FSMContext, func: typing.Any):
        """
        :param func: return: message: types.Message
        """
        data = await state.get_data()
        state_msg_id = data.get('items_management_msg_id')
        await delete_previous_messages(tgtype=message, msg_ids=state_msg_id)
        async with state.proxy():
            if not message.text.startswith('/'):
                await state.finish()
                await func()
                await self.post_proccess_func(message.from_user.id)
            elif await command_cancel.check(message):
                await state.finish()
                await self.pre_proccess_func(message.from_user.id)
            else:
                await message.answer(user_state_incorrect_input_TEXT)

    async def add_item(self, message: types.Message, state: FSMContext, func):
        await self.__state_handler(message, state, func)

    async def update_item(self, message: types.Message, state: FSMContext, func):
        await self.__state_handler(message, state, func)

    async def delete_item(self, message: types.Message, state: FSMContext, func):
        await self.__state_handler(message, state, func)