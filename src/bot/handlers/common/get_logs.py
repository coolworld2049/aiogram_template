import pathlib
from datetime import datetime

from aiogram import types

from bot import config
from bot.config import LOG_PATH
from bot.models.role.role import UserRole
from bot.models.verify import verifyUserModel
from core import dispatcher
from bot.filters.command_filters import command_get_logs
from bot.utils.chat_mgmt import save_message, delete_previous_messages
import shutil


def reg_get_logs_handler():
    dispatcher.register_message_handler(get_logs, command_get_logs)


@dispatcher.message_handler(command_get_logs)
async def get_logs(message: types.Message):
    verify_user = await verifyUserModel.verify(message.from_user.id)
    if verify_user['role'] in [UserRole.ADMIN, UserRole.MANAGER]:
        await delete_previous_messages(tgtype=message)
        out_path = f"/tmp/{config.PROJECT_NAME}_logs {datetime.today().strftime('%d_%m_%Y')}"
        path = shutil.make_archive(out_path, 'zip', LOG_PATH)
        message = await message.answer_document(types.InputFile(path))
        await save_message(message.from_user.id, message.message_id)
        pathlib.Path(out_path).unlink(missing_ok=True)
