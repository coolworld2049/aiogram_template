from aiogram import types

from config import PATH_TO_LOG_FILE
from core import dp
from filters.command_filters import command_get_logs
from models.admin.model import adminModel
from utils.chat_mgmt import save_message, delete_previous_messages


def reg_get_logs_handler():
    dp.register_message_handler(get_logs, command_get_logs)


@dp.message_handler(command_get_logs)
async def get_logs(message: types.Message):
    if await adminModel.approve_as_admin(message.from_user.id, message):
        await delete_previous_messages(tgtype=message)
        message = await message.answer_document(types.InputFile("log.log"))
        await save_message(message.from_user.id, message.message_id)
