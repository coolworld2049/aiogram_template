from bot.config import MESSAGE_DELAY
from helpers.bot.chat_mgmt import delete_message_handler, get_last_message


async def contractor_account_message_IK(user_id: int):
    await delete_message_handler(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    pass
