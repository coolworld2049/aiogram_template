from aiogram import types

from config import PATH_TO_LOG_FILE
from core import dp
from data.database.db_api import is_admin
from utils.chat_mgmt import save_message


def reg_get_logs_handler():
    dp.register_message_handler(get_logs, commands=['get_logs'])


@dp.message_handler(commands=['get_logs'])
async def get_logs(message: types.Message):
    if await is_admin(message.from_user.id):
        message = await message.answer_document(types.InputFile(PATH_TO_LOG_FILE))
        await save_message(message.from_user.id, message.message_id)
