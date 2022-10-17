import logging
import pathlib
from datetime import datetime

import loguru

from bot import config
from bot.config import LOG_PATH, LOG_FILE


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
    pathlib.Path(LOG_PATH).mkdir(parents=True, exist_ok=True)
    fmt = "{time}, {name}, {level}, {message}"
    loguru.logger.add(LOG_PATH + LOG_FILE, rotation="1024 MB", level="INFO", format=fmt, colorize=True, enqueue=True)
    logging.basicConfig(handlers=[InterceptHandler()], level=config.LOGGING_LEVEL)
