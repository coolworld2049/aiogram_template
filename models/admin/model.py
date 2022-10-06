import typing
from contextlib import suppress

from aiogram import types
from aiogram.dispatcher import FSMContext

from config import admin_items_mgmt_actionADD_TEXT_pre, admin_items_mgmt_actionUPDATE_TEXT_pre, \
    admin_items_mgmt_actionDELETE_TEXT_pre, ADMINS, admin_commands, approve_as_admin_incorrect_passphrase_TEXT, \
    navigation_BTN_back, navigation_BTN_back_to_menu
from config import admin_panel_TEXT, admin_panel_BTN_TEXT, admin_items_mgmt_message_IK_TEXT, \
    admin_items_mgmt_message_IK_TEXT_error
from config import user_state_incorrect_input_TEXT, admin_items_mgmt_actionADD_TEXT_past, \
    admin_items_mgmt_actionUPDATE_TEXT_past, admin_items_mgmt_actionDELETE_TEXT_past
from core import dp, bot, asyncPostgresModel
from filters.callback_filters import admin_cb, back_cb
from filters.command_filters import command_admin
from filters.command_filters import command_cancel
from models.database.db_api import fetchone_user
from states.AdminStates import AdminStates
from utils.bot_mgmt import set_my_commands
from utils.chat_mgmt import delete_previous_messages, save_message


class AdminPanel:
    @staticmethod
    async def _admin_panel(message: types.Message):
        user = await fetchone_user(message.from_user.id)
        if user and user['is_admin'] is False or user['is_admin'] is None:
            await delete_previous_messages(tgtype=message)
            if await AdminPanel.approve_as_admin(message.from_user.id, message):
                await AdminModel.admin_panel_message_IK(message.from_user.id)
        else:
            await AdminModel.admin_panel_message_IK(message.from_user.id)

    @staticmethod
    @dp.message_handler(command_admin)
    async def admin_panel_ms(message: types.Message):
        await AdminPanel._admin_panel(message)

    @staticmethod
    @dp.callback_query_handler(back_cb.filter(to='admin-panel'))
    async def admin_panel_cb(message: types.Message):
        await AdminPanel._admin_panel(message)

    @staticmethod
    async def approve_as_admin(user_id: int, message: types.Message) -> bool:
        user = await fetchone_user(user_id)
        if user:
            query = '''SELECT bot.upsert_table_user($1, $2)'''
            for username, passphrase in ADMINS.items():
                with suppress(AttributeError):
                    user_passphrase = message.text.split(' ')[-1]
                    if user and user['username'] == username and user_passphrase == passphrase:
                        if user['is_admin'] in [False, None]:
                            await set_my_commands(users_id=user_id, command_list=admin_commands)
                        await asyncPostgresModel.executeone(query, [user_id, True])
                        return True
                    elif user_passphrase != passphrase:
                        await message.answer(approve_as_admin_incorrect_passphrase_TEXT)
                        return False
                    else:
                        await asyncPostgresModel.executeone(query, [user_id, False])
                        return False

    @staticmethod
    async def admin_panel_message_IK(user_id: int):
        await delete_previous_messages(user_id)
        IK = types.InlineKeyboardMarkup() \
            .add(types.InlineKeyboardButton(admin_panel_BTN_TEXT,
                                            callback_data=admin_cb.new(action='None')))
        message = await bot.send_message(user_id, admin_panel_TEXT, reply_markup=IK)
        await save_message(user_id, message.message_id)

    @staticmethod
    async def admin_items_mgmt_message_IK(user_id: int):
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


class AdminModel(AdminPanel):
    def __init__(self):
        self.message = None
        self.state = None

    def __reg_item_mgmgt_handlers(self):
        dp.register_message_handler(self.admin_panel_ms, command_admin)
        dp.register_callback_query_handler(self.admin_panel_cb, back_cb.filter())
        dp.register_callback_query_handler(self.admin_items_handler, admin_cb.filter())
        dp.register_message_handler(self.add_item_hd, state=AdminStates.add_item)
        dp.register_message_handler(self.update_item_hd, state=AdminStates.update_item)
        dp.register_message_handler(self.delete_item_hd, state=AdminStates.delete_item)

    async def __add(self):
        ...
        await self.message.answer(admin_items_mgmt_actionADD_TEXT_past)

    async def __update(self):
        ...
        await self.message.answer(admin_items_mgmt_actionUPDATE_TEXT_past)

    async def __delete(self):
        ...
        await self.message.answer(admin_items_mgmt_actionDELETE_TEXT_past)

    async def __controller(self, func: typing.Any):
        """
        :param func: return: message: types.Message
        """
        data = await self.state.get_data()
        state_msg_id = data.get('items_management_msg_id')
        await delete_previous_messages(by_user_id=self.message.from_user.id, msg_ids=state_msg_id)
        async with self.state.proxy():
            if not self.message.text.startswith('/'):
                await self.state.finish()
                await func()
                await self.admin_items_mgmt_message_IK(self.message.from_user.id)
            elif await command_cancel.check(self.message):
                await self.state.finish()
                await self.admin_panel_message_IK(self.message.from_user.id)
            else:
                await self.message.answer(user_state_incorrect_input_TEXT)

    async def _add_item_cnt(self, message: types.Message, state: FSMContext):
        self.message = message
        self.state = state
        await self.__controller(self.__add)

    async def _update_item_cnt(self, message: types.Message, state: FSMContext):
        self.message = message
        self.state = state
        await self.__controller(self.__update)

    async def _delete_item_cnt(self, message: types.Message, state: FSMContext):
        self.message = message
        self.state = state
        await self.__controller(self.__delete)

    def get_admin_handlers(self):
        return self.__reg_item_mgmgt_handlers

    @staticmethod
    @dp.callback_query_handler(admin_cb.filter())
    async def admin_items_handler(callback_query: types.CallbackQuery, callback_data: dict):
        await delete_previous_messages(tgtype=callback_query)
        action = callback_data.get('action')
        text = str()
        if action == 'add':
            text = admin_items_mgmt_actionADD_TEXT_pre
            await AdminStates.add_item.set()
        elif action == 'update':
            text = admin_items_mgmt_actionUPDATE_TEXT_pre
            await AdminStates.update_item.set()
        elif action == 'delete':
            text = admin_items_mgmt_actionDELETE_TEXT_pre
            await AdminStates.delete_item.set()

        if action != 'None':
            message = await bot.send_message(callback_query.from_user.id, text,
                                             parse_mode=types.ParseMode.MARKDOWN)
            await dp.current_state(chat=callback_query.from_user.id, user=callback_query.from_user.id) \
                .update_data({'items_management_msg_id': f"{message.message_id}"})
        elif action == 'None':
            await AdminModel.admin_items_mgmt_message_IK(callback_query.from_user.id)

    @staticmethod
    @dp.message_handler(state=AdminStates.add_item)
    async def add_item_hd(message: types.Message, state: FSMContext):
        await AdminModel()._add_item_cnt(message, state)

    @staticmethod
    @dp.message_handler(state=AdminStates.update_item)
    async def update_item_hd(message: types.Message, state: FSMContext):
        await AdminModel()._update_item_cnt(message, state)

    @staticmethod
    @dp.message_handler(state=AdminStates.delete_item)
    async def delete_item_hd(message: types.Message, state: FSMContext):
        await AdminModel()._delete_item_cnt(message, state)


adminModel = AdminModel()