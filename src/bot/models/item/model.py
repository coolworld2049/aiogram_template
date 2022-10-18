import typing

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.filters.command_filters import command_cancel
from bot.models.role.role import UserRole
from bot.strings.answer_blanks import user_state_incorrect_input_TEXT
from helpers.bot.chat_mgmt import delete_previous_messages


class ItemManagerModel:
    __slots__ = ('pre_proccess_func', 'post_proccess_func')

    def __init__(self, pre_proccess_func, post_proccess_func):
        """
        async def pre_admin_panel_message_IK(user_id: int):
            await delete_previous_messages(user_id)

            async def _panel():
                cb = item_cb.new(action='None', callback=command_admin.commands[0])
                btn_panel = types.InlineKeyboardButton(admin_panel_BTN_items_mgmt_TEXT, callback_data=cb)
                btn_server_stats = types.InlineKeyboardButton(admin_panel_BTN_server_stats_TEXT,
                                                              callback_data=server_stats_cb.new())
                IK = types.InlineKeyboardMarkup().add(btn_panel, btn_server_stats)
                msg = await bot.send_message(user_id, admin_panel_TEXT, reply_markup=IK)
                await save_message(user_id, msg.message_id)

            verify_result = await verifyUserModel.verify(user_id)
            if verify_result['role'] == UserRole.ADMIN or verify_result['user_id'] in config.ADMINS:
                await _panel()

        async def post_user_mgmt_message_IK(user_id: int):
            await delete_previous_messages(user_id)
            IK = types.InlineKeyboardMarkup(row_width=2)
            example_items = await fetchall_user()
            if example_items and len(example_items) > 0:
                for ex_item in example_items:
                    if ex_item['user_id'] != user_id:
                        text = f"{ex_item['username']} | role: {ex_item['role']}"
                        item_callback = f"{user_id}_edit_{ex_item['user_id']}"
                        IK.row(types.InlineKeyboardButton(text, callback_data=item_cb.new(action='update',
                                                                                          callback=item_callback)))
                IK.row(types.InlineKeyboardButton('➕', callback_data=item_cb.new(action='add', callback='None')),
                       types.InlineKeyboardButton('➖', callback_data=item_cb.new(action='delete', callback='None')))
                IK.row(types.InlineKeyboardButton(navigation_BTN_back,
                                                  callback_data=back_cb.new(to=UserRole.ADMIN, msg_ids='None')))
                message = await bot.send_message(user_id, items_mgmt_message_IK_TEXT, reply_markup=IK,
                                                 parse_mode=types.ParseMode.MARKDOWN)
                await save_message(user_id, message.message_id)
            else:
                message = await bot.send_message(user_id, items_mgmt_message_IK_TEXT_error, reply_markup=IK)
                await save_message(user_id, message.message_id)
        """
        self.pre_proccess_func = pre_proccess_func
        self.post_proccess_func = post_proccess_func

    async def __state_handler(self, tgtype: types.Message | types.CallbackQuery, state: FSMContext,
                              func: typing.Any, role: UserRole):
        data = await state.get_data()
        state_msg_id = data.get('items_management_msg_id')
        await delete_previous_messages(tgtype=tgtype, msg_ids=state_msg_id)
        async with state.proxy():
            check = await command_cancel.check(tgtype) if isinstance(tgtype, types.Message)\
                else tgtype.data == command_cancel.commands[0]
            if not check:
                await state.finish()
                await func(tgtype, state)
                await self.post_proccess_func(tgtype.from_user.id, role)
            elif check:
                await state.finish()
                await self.pre_proccess_func(tgtype.from_user.id, role)
            else:
                await tgtype.answer(user_state_incorrect_input_TEXT)

    async def add_item(self, message: types.Message, state: FSMContext, func, role: UserRole):
        await self.__state_handler(message, state, func, role)

    async def update_item(self, message: types.Message, state: FSMContext, func, role: UserRole):
        await self.__state_handler(message, state, func, role)

    async def delete_item(self, message: types.Message, state: FSMContext, func, role: UserRole):
        await self.__state_handler(message, state, func, role)
