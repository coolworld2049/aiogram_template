import asyncio
import logging

import asyncpg

from config import PG_DSN

pool: asyncpg.Pool = asyncio.get_event_loop().run_until_complete(asyncpg.create_pool(PG_DSN))


async def executeone(query: str, values: list):
    async with pool.acquire() as connection:
        async with connection.transaction():
            tr = connection.transaction()
            res = None
            await tr.start()
            try:
                if values:
                    res = await connection.execute(query, *values)
            except Exception as e:
                logging.error(f"transaction: Exception: {e.args}")
                await tr.rollback()
            else:
                await tr.commit()
            return res


async def executemany(command: str, list_of_values: list):
    async with pool.acquire() as connection:
        async with connection.transaction():
            tr = connection.transaction()
            res = None
            await tr.start()
            try:
                if list_of_values:
                    res = await connection.executemany(command, list_of_values)
            except Exception as e:
                logging.error(f"transaction: Exception: {e.args}")
                await tr.rollback()
            else:
                await tr.commit()
            return res


async def fetchone(query: str, values: list = None):
    res = await fetchmany(query, values)
    return res[0] if res and len(res) > 0 else res


async def fetchmany(query: str, values: list = None):
    async with pool.acquire() as connection:
        async with connection.transaction():
            tr = connection.transaction()
            res = None
            await tr.start()
            try:
                if values:
                    res = await connection.fetch(query, *values)
                else:
                    res = await connection.fetch(query)
            except Exception as e:
                logging.error(f"transaction: Exception: {e.args}")
                await tr.rollback()
            else:
                await tr.commit()
            return res
