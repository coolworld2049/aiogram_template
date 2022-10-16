from aiogram import types

from bot.models.verify import verifyUserModel
from core import dispatcher
from bot.filters.command_filters import command_get_logs
from bot.utils.chat_mgmt import save_message, delete_previous_messages


def reg_get_logs_handler():
    dispatcher.register_message_handler(get_logs, command_get_logs)


@dispatcher.message_handler(command_get_logs)
async def get_logs(message: types.Message):
    verify_result = await verifyUserModel.verify(message.from_user.id)
    if verify_result['is_admin'] or verify_result['is_manager']:
        await delete_previous_messages(tgtype=message)
        message = await message.answer_document(types.InputFile("log.log"))
        await save_message(message.from_user.id, message.message_id)
