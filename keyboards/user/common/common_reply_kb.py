from aiogram import types


def RK_verify_phone():
    RK = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        types.KeyboardButton('📲 Подтвердить', request_contact=True),
        types.KeyboardButton('😑 Осмотреться'))
    return RK


async def cancel_button_message_RK(button: types.KeyboardButton = None):
    RK = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if button:
        RK.insert(button)
    RK.insert(types.KeyboardButton('❌ Отмена'))
    return RK
