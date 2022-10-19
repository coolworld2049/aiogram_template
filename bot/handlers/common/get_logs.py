import pathlib
import shutil
from datetime import datetime

from aiogram import types
from loguru import logger

from bot.config import LOG_PATH
from bot.filters.command_filters import command_logs
from bot.models.role.role import UserRole
from bot.models.verify import verifyUserModel
from bot.utils.chat_mgmt import save_message, delete_previous_messages
from core import dispatcher


def reg_get_logs_handler():
    dispatcher.register_message_handler(get_logs, command_logs)


@dispatcher.message_handler(command_logs)
async def get_logs(message: types.Message):
    verify_user = await verifyUserModel.verify(message.from_user.id)
    if verify_user['role'] in [UserRole.ADMIN, UserRole.MANAGER]:
        await delete_previous_messages(tgtype=message)
        filename = f"{LOG_PATH.split('/')[0]}-{datetime.today().strftime('%d_%m_%Y')}"
        out_path = f"/tmp/{filename}"
        path = shutil.make_archive(out_path, 'zip', LOG_PATH, logger=logger)
        message = await message.answer_document(types.InputFile(path))
        await save_message(message.from_user.id, message.message_id)
        pathlib.Path(out_path + '.zip').unlink()
        logger.info(f"user_id: {message.from_user.id}: zip file out_path: {out_path}")
