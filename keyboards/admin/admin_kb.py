from aiogram import types

from core import bot


async def admin_panel_message_IK(user_id: int):
    IK = types.InlineKeyboardMarkup() \
        .add(types.InlineKeyboardButton('Управление элементами', callback_data="item-management"))
    await bot.send_message(user_id, 'Админ панель', reply_markup=IK)


async def items_management_message_IK(user_id: int):
    IK = types.InlineKeyboardMarkup(row_width=2)
    items = ...
    if len(items) > 0:
        for item in items:
            callback_data = f"admin_update-item_..."
            item_text = f"{item[...]}"
            IK.insert(types.InlineKeyboardButton(item_text, callback_data=callback_data))
        IK.row(types.InlineKeyboardButton('add', callback_data=f"admin_add-item"),
               types.InlineKeyboardButton('del', callback_data=f"admin_delete-item"))
        await bot.send_message(user_id, "Здесь вы можете редактировать список *элементов*",
                               parse_mode=types.ParseMode.MARKDOWN_V2,
                               reply_markup=IK)
    else:
        await bot.send_message(user_id, f"Список элементов отсутствует в базе данных", reply_markup=IK)
