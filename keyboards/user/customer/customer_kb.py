from config import MESSAGE_DELAY
from utils.chat_mgmt import get_last_message, delete_message


async def customer_account_message_IK(user_id: int):
    await delete_message(user_id, await get_last_message(user_id), MESSAGE_DELAY)
    pass
