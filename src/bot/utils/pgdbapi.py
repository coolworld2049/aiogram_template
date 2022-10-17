from datetime import datetime

from aiogram.types import User

from bot.models.database import asyncPostgresModel
from bot.models.role.role import UserRole
from bot.states.UserStates import UserStates


async def save_user(user: User):
    query = '''INSERT INTO schema.user(user_id, username, "role", last_seen) VALUES($1,$2,$3,$4) 
    ON CONFLICT DO NOTHING'''
    values = [
        user.id,
        user.username,
        UserRole.USER,
        datetime.timestamp(datetime.now())
    ]
    result = await asyncPostgresModel.executeone(query, values)
    if not result or len(result) == 0:
        return None
    else:
        return result


async def update_user(user: User, f_name: str, l_name: str):
    query = '''UPDATE schema.user SET first_name = $2, last_name = $3, last_seen = $4 WHERE user_id = $1'''
    values = [
        user.id,
        f_name,
        l_name,
        datetime.timestamp(datetime.now())
    ]
    result = await asyncPostgresModel.executeone(query, values)
    if not result or len(result) == 0:
        return None
    else:
        return result


async def fetchone_user(user_id: int):
    query = '''SELECT * FROM schema."user" WHERE user_id = $1'''
    result = await asyncPostgresModel.fetchone(query, [user_id])
    if not result or len(result) == 0:
        return None
    else:
        return result


async def fetchall_user():
    result = await asyncPostgresModel.fetchmany('''SELECT * FROM schema."user"''')
    if not result or len(result) == 0:
        return None
    else:
        return result


async def fetchall_user_ids():
    result = await asyncPostgresModel.fetchmany('''SELECT user_id FROM schema."user"''')
    if not result or len(result) == 0:
        return None
    else:
        return result


async def fetchone_order(order_id: int):
    query = '''SELECT * FROM schema."order" WHERE id = $1'''
    result = await asyncPostgresModel.fetchone(query, [order_id])
    if not result or len(result) == 0:
        return None
    else:
        return result


async def fetchone_last_order_id():
    query = '''SELECT id FROM schema."order" ORDER BY id DESC LIMIT 1'''
    res = await asyncPostgresModel.fetchone(query)
    return res['id'] + 1 if res and len(res) > 0 else 0


async def fetchone_temp(user_id: int):
    query = '''SELECT last_message_id FROM schema.temp WHERE user_id = $1'''
    result = await asyncPostgresModel.fetchone(query, [user_id])
    if not result or len(result) == 0:
        return None
    else:
        return result


async def check_user_active_orders(user_id: int):
    values = [user_id, UserStates.ACCEPTED.state, UserStates.PROGRESS.state]
    cs_query = '''
            SELECT count(*) FROM schema.order WHERE customer_id = $1 AND state = $2 
            OR state = $3'''
    customer_has_orders = await asyncPostgresModel.fetchone(cs_query, values)

    ct_query = '''
            SELECT count(*) FROM schema.order WHERE customer_id = $1 AND state = $2
            OR state = $3'''
    contractor_has_orders = await asyncPostgresModel.fetchone(ct_query, values)

    return {'customer_has_orders': True if customer_has_orders['count'] else False,
            'contractor_has_orders': True if contractor_has_orders['count'] else False}

