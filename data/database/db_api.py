from datetime import datetime

from aiogram.types import User

from config import ADMINS
from core import logger
from data.database.database import executeone, fetchone
from states.UserStates import UserStates


async def save_user(user: User):
    query = '''INSERT INTO bot.user(user_id, username, is_admin, last_seen) VALUES($1,$2,$3,$4)
    ON CONFLICT DO NOTHING'''
    values = [
        user.id,
        user.username,
        None,
        datetime.timestamp(datetime.now())
    ]
    result = await executeone(query, values)
    if not result:
        logger.info(f"save_user: INSERT CONFLICT")
    return result


async def update_user(user: User, f_name: str, l_name: str):
    query = '''UPDATE bot.user SET first_name = $2, last_name = $3, last_seen = $4 WHERE user_id = $1'''
    values = [
        user.id,
        f_name,
        l_name,
        datetime.timestamp(datetime.now())
    ]
    result = await executeone(query, values)
    if not result:
        logger.info(f"update_user: CONFLICT")
    return result


async def fetchone_user(user_id: int):
    query = '''SELECT * FROM bot."user" WHERE user_id = $1'''
    result = await fetchone(query, [user_id])
    if not result:
        logger.info(f"fetchone_user: CONFLICT")
        return result
    else:
        return result


async def fetchone_order(order_id: int):
    query = '''SELECT * FROM bot."order" WHERE id = $1'''
    result = await fetchone(query, [order_id])
    if not result:
        logger.info(f"fetchone_order: CONFLICT")
        return result
    else:
        return result


async def fetchone_last_order_id():
    query = '''SELECT id FROM bot."order" ORDER BY id DESC LIMIT 1'''
    res = await fetchone(query)
    return res['id'] + 1 if res and len(res) > 0 else 0


async def check_user_active_orders(user_id: int):
    values = [user_id, UserStates.accepted.state, UserStates.progress.state]
    cs_query = '''
            SELECT count(*) FROM bot.order WHERE customer_id = $1 AND role = 'sender' AND state = $2 
            OR state = $3'''
    customer_has_orders = await fetchone(cs_query, values)

    ct_query = '''
            SELECT count(*) FROM bot.order WHERE customer_id = $1 AND role = 'traveler' AND state = $2
            OR state = $3'''
    contractor_has_orders = await fetchone(ct_query, values)

    return {'customer_has_orders': True if customer_has_orders['count'] else False,
            'contractor_has_orders': True if contractor_has_orders['count'] else False}


async def is_admin(user_id: int):
    users = [await fetchone_user(user_id)]
    if len(users) != 0:
        for us in users:
            query = '''SELECT bot.upsert_table_user($1, $2)'''
            if us['username'] in ADMINS:
                await executeone(query, [user_id, True])
                return True
            else:
                await executeone(query, [user_id, False])
                return False
