import asyncio
import logging

import asyncpg
from asyncpg import Connection

from config import PG_DSN


class AsyncPostgresModel:
    def __init__(self, DSN: str):
        self.DSN: str = DSN
        self.pool: asyncpg.Pool = asyncio.get_event_loop().run_until_complete(asyncpg.create_pool(PG_DSN))

    @staticmethod
    async def transaction_wrapper(connection: Connection, func):
        try:
            async with connection.transaction():
                tr = connection.transaction()
                res = None
                await tr.start()
                try:
                    res = await func()
                except asyncpg.TransactionIntegrityConstraintViolationError as e:
                    logging.error(f"transaction_wrapper: connection: TransactionIntegrityConstraintViolationError:"
                                  f" {e.args}: TRANSACTION CANCELED")
                    await tr.rollback()
                except asyncpg.TransactionRollbackError as e:
                    logging.error(f"transaction_wrapper: connection: TransactionRollbackError: {e.args}:"
                                  f" TRANSACTION CANCELED")
                    await tr.rollback()
                else:
                    await tr.commit()
                return res
        except asyncpg.PostgresConnectionError as e:
            logging.warning(f"transaction_wrapper: connection: PostgresError: {e.args}: CONNECTION ERROR")

    async def executeone(self, query: str, values: list):
        async with self.pool.acquire() as connection:
            async def _executeone():
                return await connection.execute(query, *values) if values else None

            return await self.transaction_wrapper(connection, _executeone)

    async def executemany(self, command: str, list_of_values: list):
        async with self.pool.acquire() as connection:
            async def _executemany():
                return await connection.executemany(command, list_of_values) if list_of_values else None

            return await self.transaction_wrapper(connection, _executemany)

    async def fetchone(self, query: str, values: list = None):
        res = await self.fetchmany(query, values)
        return res[0] if res and len(res) > 0 else res

    async def fetchmany(self, query: str, values: list = None):
        async with self.pool.acquire() as connection:
            async def _fetchmany():
                return await connection.fetch(query, *values) if values else await connection.fetch(query)

            return await self.transaction_wrapper(connection, _fetchmany)
