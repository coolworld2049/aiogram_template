from aiogram import types
from aiogram.dispatcher import FSMContext

from core import bot


async def admin_panel_message_IK(user_id: int):
    IK = types.InlineKeyboardMarkup() \
        .add(types.InlineKeyboardButton('Управление элементами', callback_data=f"{user_id}_admin-items-management"))
    await bot.send_message(user_id, 'Админ панель', reply_markup=IK)


async def admin_items_management_message_IK(user_id: int):
    IK = types.InlineKeyboardMarkup(row_width=2)
    items = ['item 1', 'item 2', 'item 3', 'item 4']
    if items and len(items) > 0:
        for item in items:
            callback_data = f"{user_id}_admin-items-management_update_{item}"
            item_text = f"{item}"
            IK.insert(types.InlineKeyboardButton(item_text, callback_data=callback_data))
        IK.row(types.InlineKeyboardButton('add', callback_data=f"{user_id}_admin-items-management_add"),
               types.InlineKeyboardButton('delete', callback_data=f"{user_id}_admin-items-management_delete"))
        await bot.send_message(user_id, "Здесь вы можете редактировать список *элементов*",
                               reply_markup=IK)
    else:
        await bot.send_message(user_id, f"Список элементов отсутствует в базе данных", reply_markup=IK)


async def check_command_cancel(message: types.Message):
    return message.get_command(pure=True) in ['cancel', 'start']


async def admin_add_item_controller(message: types.Message, state: FSMContext):
    async with state.proxy():
        check = await check_command_cancel(message)
        if not message.text.startswith('/'):
            await state.finish()
            await message.answer('added')
        elif check:
            await state.finish()
            await message.answer(f'{message.get_command()}')
        else:
            await message.answer('Неправильный формат ввода')
    await admin_items_management_message_IK(message.from_user.id)


async def admin_update_item_controller(message: types.Message, state: FSMContext):
    async with state.proxy():
        check = await check_command_cancel(message)
        if not message.text.startswith('/'):
            await state.finish()
            await message.answer('updated')
        elif check:
            await state.finish()
            await message.answer(f'{message.get_command()}')
        else:
            await message.answer('Неправильный формат ввода')
    await admin_items_management_message_IK(message.from_user.id)


async def admin_delete_item_controller(message: types.Message, state: FSMContext):
    async with state.proxy():
        check = await check_command_cancel(message)
        if not message.text.startswith('/'):
            await state.finish()
            await message.answer('deleted')
        elif check:
            await state.finish()
            await message.answer(f'{message.get_command()}')
        else:
            await message.answer('Неправильный формат ввода')
    await admin_items_management_message_IK(message.from_user.id)
