from aiogram import types

from config import PATH_TO_LOG_FILE
from core import dp
from models.database.db_api import user_is_admin
from filters.command_filters import command_get_logs
from utils.chat_mgmt import save_message, delete_previous_messages


def reg_get_logs_handler():
    dp.register_message_handler(get_logs, command_get_logs)


@dp.message_handler(command_get_logs)
async def get_logs(message: types.Message):
    if await user_is_admin(message.from_user.id):
        await delete_previous_messages(tgtype=message)
        message = await message.answer_document(types.InputFile(PATH_TO_LOG_FILE))
        await save_message(message.from_user.id, message.message_id)
