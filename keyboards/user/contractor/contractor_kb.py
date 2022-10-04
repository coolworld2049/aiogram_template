from config import MESSAGE_DELAY
from utils.chat_mgmt import del_message, get_last_message


async def contractor_account_message_IK(user_id: int):
    await del_message(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    pass
