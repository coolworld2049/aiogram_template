from aiogram import types
from aiogram.dispatcher import FSMContext

from core import bot
from filters.callback_filters import admin_cb
from utils.chat_mgmt import delete_previous_messages, save_message


async def admin_panel_message_IK(user_id: int):
    IK = types.InlineKeyboardMarkup() \
        .add(types.InlineKeyboardButton('Управление элементами', callback_data=admin_cb.new(action='None')))
    await bot.send_message(user_id, 'Админ панель', reply_markup=IK)


async def admin_items_management_message_IK(user_id: int):
    await delete_previous_messages(user_id)
    IK = types.InlineKeyboardMarkup(row_width=2)
    items = ['item 1', 'item 2', 'item 3', 'item 4']
    if items and len(items) > 0:
        for item in items:
            item_text = f"{item}"
            IK.insert(types.InlineKeyboardButton(item_text, callback_data=admin_cb.new(action='update')))
        IK.row(types.InlineKeyboardButton('add', callback_data=admin_cb.new(action='update')),
               types.InlineKeyboardButton('delete', callback_data=admin_cb.new(action='delete')))
        message = await bot.send_message(user_id, "Здесь вы можете редактировать список *элементов*",
                                         reply_markup=IK)
        await save_message(user_id, message.message_id)
    else:
        message = await bot.send_message(user_id, f"Список элементов отсутствует в базе данных",
                                         reply_markup=IK)
        await save_message(user_id, message.message_id)


async def check_command_cancel(message: types.Message):
    return message.get_command(pure=True) in ['cancel']


async def admin_add_item_controller(message: types.Message, state: FSMContext):
    async with state.proxy():
        ch_cancel = await check_command_cancel(message)
        if not message.text.startswith('/'):
            await state.finish()
            await message.answer('added')
            await admin_items_management_message_IK(message.from_user.id)
        elif ch_cancel:
            await state.finish()
            await message.answer(f'{message.get_command()}')
            await admin_panel_message_IK(message.from_user.id)
        else:
            await message.answer('Неправильный формат ввода')


async def admin_update_item_controller(message: types.Message, state: FSMContext):
    async with state.proxy():
        ch_cancel = await check_command_cancel(message)
        if not message.text.startswith('/'):
            await state.finish()
            await message.answer('updated')
            await admin_items_management_message_IK(message.from_user.id)
        elif ch_cancel:
            await state.finish()
            await message.answer(f'{message.get_command()}')
            await admin_panel_message_IK(message.from_user.id)
        else:
            await message.answer('Неправильный формат ввода')


async def admin_delete_item_controller(message: types.Message, state: FSMContext):
    async with state.proxy():
        ch_cancel = await check_command_cancel(message)
        if not message.text.startswith('/'):
            await state.finish()
            await message.answer('deleted')
            await admin_items_management_message_IK(message.from_user.id)
        elif ch_cancel:
            await state.finish()
            await message.answer(f'{message.get_command()}')
            await admin_panel_message_IK(message.from_user.id)
        else:
            await message.answer('Неправильный формат ввода')
