from datetime import datetime

from aiogram.types import User

from core import logger
from data.database.database import executeone, fetchone
from states.OrderStates import OrderStates


async def insert_user(user: User):
    query = '''INSERT INTO bot.user(user_id, username, agree_with_rules, last_seen) VALUES($1,$2,$3,$4)
    ON CONFLICT DO NOTHING'''
    values = [
        user.id,
        user.username,
        True,
        datetime.timestamp(datetime.now())
    ]
    result = await executeone(query, values)
    if not result:
        logger.info(f"insert_user: FAILURE")
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
        logger.info(f"update_user: FAILURE")
    return result


async def insert_customer(user: User):
    query = '''INSERT INTO bot.customer(user_id, last_seen) VALUES($1,$2) ON CONFLICT DO NOTHING'''
    values = [
        user.id,
        datetime.timestamp(datetime.now())
    ]
    result = await executeone(query, values)
    if not result:
        logger.info(f"insert_customer: FAILURE")
    return result


async def insert_contractor(user: User):
    query = '''INSERT INTO bot.contractor(user_id, last_seen) VALUES($1,$2) ON CONFLICT DO NOTHING'''
    values = [
        user.id,
        datetime.timestamp(datetime.now())
    ]
    result = await executeone(query, values)
    if not result:
        logger.info(f"insert_customer: FAILURE")
    return result


async def fetchone_user(user_id: int):
    query = '''SELECT * FROM bot."user" WHERE user_id = $1'''
    result = await fetchone(query, [user_id])
    if not result:
        logger.info(f"fetchone_user: FAILURE")
        return result
    else:
        return result


async def fetchone_order(order_id: int):
    query = '''SELECT * FROM bot."order" WHERE id = $1'''
    result = await fetchone(query, [order_id])
    if not result:
        logger.info(f"fetchone_order: FAILURE")
        return result
    else:
        return result

async def fetchone_last_order_id():
    query = '''SELECT id FROM bot."order" ORDER BY id DESC LIMIT 1'''
    res = await fetchone(query)
    return res['id'] + 1 if len(res) > 0 else 0


async def check_user_active_orders(user_id: int):
    """
    check by:\n
    'state_one': OrderStates.order_accepted.state,\n
    'state_two': OrderStates.order_in_work.state,\n
    :param user_id:
    :return: {'customer_has_orders': bool, 'contractor_has_orders': bool}
    """
    values = [
        user_id,
        OrderStates.order_accepted.state,
        OrderStates.order_in_work.state,
    ]
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
