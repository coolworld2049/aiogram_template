import asyncio
from contextlib import suppress

from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound, MessageIdentifierNotSpecified

from config import DEBUG_MODE, MESSAGE_DELAY
from core import bot, logger, asyncPostgresModel
from models.database.db_api import fetchone_temp


async def save_message(user_id: int, message_id: int):
    await asyncPostgresModel.executeone('''SELECT bot.upsert_table_temp($1, $2)''', [user_id, str(message_id)])
    if DEBUG_MODE:
        logger.info(f"save_message: user_id: {user_id}: message_id: {message_id}")


async def del_message(chat_id: int, message_id: str, sleep_time: float = 0):
    """
    :param chat_id:
    :param message_id: "123,124,125" or "123-125" or "123"
    :param sleep_time:
    :return: message_action_delay from config.py
    """
    if message_id:
        await asyncio.sleep(sleep_time)
        with suppress(MessageCantBeDeleted, MessageToDeleteNotFound, MessageIdentifierNotSpecified, ValueError,
                      KeyError):
            if '-' in message_id:
                _message_id = message_id.split('-')
                start = int(_message_id[0])
                stop = int(_message_id[1]) + 2
                for item in range(start, stop):
                    if item != 'None' and item != '':
                        with suppress(MessageToDeleteNotFound):
                            await bot.delete_message(chat_id, item)
            else:
                _message_id = message_id.split(',')
                if len(_message_id) > 1:
                    for item in _message_id:
                        if item != 'None' and item != '':
                            with suppress(MessageToDeleteNotFound):
                                await bot.del_message(chat_id, item)
                else:
                    if message_id != 'None' and message_id != '' and message_id != ' ':
                        await bot.delete_message(chat_id, message_id)
    elif DEBUG_MODE:
        logger.error(f'delete_last_message: chat_id: {chat_id}: FAILED: message_id is None')


async def delete_previous_messages(by_user_id: int = None, msg_ids: str = None,
                                   tgtype: types.CallbackQuery | types.Message = None):
    with suppress(MessageToDeleteNotFound):
        if tgtype:
            if isinstance(tgtype, types.CallbackQuery):
                await asyncio.sleep(MESSAGE_DELAY)
                await tgtype.message.delete()
                if msg_ids:
                    await del_message(tgtype.from_user.id, msg_ids, MESSAGE_DELAY)
            elif isinstance(tgtype, types.Message) and msg_ids:
                await asyncio.sleep(MESSAGE_DELAY)
                await del_message(tgtype.from_user.id, msg_ids, MESSAGE_DELAY)
        if by_user_id:
            await asyncio.sleep(MESSAGE_DELAY)
            if not msg_ids:
                await del_message(by_user_id, await get_last_message(by_user_id), MESSAGE_DELAY)
            else:
                await del_message(by_user_id, msg_ids, MESSAGE_DELAY)


async def get_last_message(user_id: int):
    res = await fetchone_temp(user_id)
    msg_id = res['last_message_id'] if res and len(res) > 0 else None
    if DEBUG_MODE:
        logger.info(f"get_last_message: user_id: {user_id}: message_id: {msg_id}")
    return msg_id
