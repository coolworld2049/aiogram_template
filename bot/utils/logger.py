import logging
import pathlib

import loguru

from bot import config
from bot.config import BASE_LOG_DIR, ERROR_LOG_PATH, BASE_LOG_PATH


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = loguru.logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


def setup_logger():
    pathlib.Path(BASE_LOG_DIR).mkdir(parents=True, exist_ok=True)
    fmt = "{time} {name} {level} {message}"
    loguru.logger.add(BASE_LOG_PATH, rotation="512 MB", level="INFO", format=fmt,
                      encoding='utf-8', colorize=True, enqueue=True)
    loguru.logger.add(ERROR_LOG_PATH, rotation="512 MB", level="ERROR", format=fmt,
                      encoding='utf-8', colorize=True, enqueue=True, serialize=True)
    logging.basicConfig(handlers=[InterceptHandler()], level=config.LOGGING_LEVEL)
