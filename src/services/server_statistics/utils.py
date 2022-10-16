import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor


async def async_wrapper(func, *args):
    try:
        loop = asyncio.get_event_loop()
        with ProcessPoolExecutor() as pool:
            return await loop.run_in_executor(pool, func, *args)
    except Exception as e:
        logging.exception(f'async_over_sync: sync func: {func.__name__}. Exception: {e.args}')
