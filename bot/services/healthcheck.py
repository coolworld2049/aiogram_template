import aioredis
from loguru import logger

from bot.models.database.postgresql.model import asyncPostgresModel


async def check_redis():
    try:
        logger.info(f"check_redis: version {aioredis.VERSION}")
    except Exception as e:
        logger.warning(f"{False, str(e)}")


async def check_postgres():
    try:
        version = await asyncPostgresModel.fetchone("select version();")
        logger.info(f"check_postgres: version {version}")
    except Exception as e:
        logger.warning(f"{False, str(e)}")


async def run_healthcheck():
    await check_redis()
    await check_postgres()
