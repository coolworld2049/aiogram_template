import asyncio
from contextlib import suppress

from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound, MessageIdentifierNotSpecified

from config import DEBUG_MODE
from core import bot, logger
from data.database.database import executeone, fetchone


async def save_message(user_id: int, message_id: int):
    await executeone('''SELECT bot.upsert_table_temp($1, $2)''', [user_id, str(message_id)])
    if DEBUG_MODE:
        logger.info(f"save_message: user_id: {user_id}: message_id: {message_id}")


async def delete_message(chat_id: int, message_id: str, sleep_time: float = 0):
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
                                await bot.delete_message(chat_id, item)
                else:
                    if message_id != 'None' and message_id != '' and message_id != ' ':
                        await bot.delete_message(chat_id, message_id)
    else:
        logger.error(f'delete_last_message: chat_id: {chat_id}: FAILED: message_id is None')


async def get_last_message(user_id: int):
    res = await fetchone('''SELECT last_message_id FROM bot.temp WHERE user_id = $1''', [user_id])
    msg_id = None
    if len(res) > 0:
        msg_id = res['last_message_id'] if len(res) > 0 else None
        if DEBUG_MODE:
            logger.info(f"get_last_message: user_id: {user_id}: message_id: {msg_id}")
    return msg_id
