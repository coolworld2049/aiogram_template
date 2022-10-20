import asyncio
import logging

import asyncpg
from asyncpg import Connection


class AsyncPostgresModel:
    __slots__ = ('DSN', 'pool')

    def __init__(self, DSN: str):
        """
        :param DSN:
        """
        self.DSN: str = DSN
        self.pool: asyncpg.Pool = asyncio.get_event_loop().run_until_complete(asyncpg.create_pool(self.DSN))

    @staticmethod
    async def __transaction_wrapper(connection: Connection, func) -> asyncpg.Record:
        try:
            async with connection.transaction():
                tr = connection.transaction()
                res = None
                await tr.start()
                try:
                    res = await func()
                except Exception as e:
                    logging.exception(f"__transaction_wrapper: transaction: Exception: {e.args}: rollback")
                    await tr.rollback()
                else:
                    await tr.commit()
                return res
        except Exception as e:
            logging.exception(f"__transaction_wrapper: connection: Exception: {e.args}: connection error")

    async def executeone(self, query: str, values: list) -> asyncpg.Record:
        async with self.pool.acquire() as connection:
            async def __executeone():
                return await connection.execute(query, *values) if values else None

            return await AsyncPostgresModel.__transaction_wrapper(connection, __executeone)

    async def executemany(self, command: str, list_of_values: list) -> asyncpg.Record:
        async with self.pool.acquire() as connection:
            async def __executemany():
                return await connection.executemany(command, list_of_values) if list_of_values else None

            return await AsyncPostgresModel.__transaction_wrapper(connection, __executemany)

    async def fetchone(self, query: str, values: list = None) -> asyncpg.Record:
        res = await self.fetchmany(query, values)
        return res[0] if res and len(res) > 0 else res

    async def fetchmany(self, query: str, values: list = None) -> asyncpg.Record:
        async with self.pool.acquire() as connection:
            async def __fetchmany():
                return await connection.fetch(query, *values) if values else await connection.fetch(query)

            return await AsyncPostgresModel.__transaction_wrapper(connection, __fetchmany)
