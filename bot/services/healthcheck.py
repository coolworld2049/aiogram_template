import aioredis
from loguru import logger

from models.database.postgresql import asyncPostgresModel


async def run_healthcheck():
    await check_redis()
    await check_postgres()


async def check_redis():
    try:
        res = f"check_redis: version {aioredis.VERSION}"
    except Exception as e:
        res = False, str(e)
    logger.info(res)


async def check_postgres():
    try:
        version = await asyncPostgresModel.fetchone("select version();")
        res = f"check_postgres: version {version}"
    except Exception as e:
        res = False, str(e)
    logger.info(res)

