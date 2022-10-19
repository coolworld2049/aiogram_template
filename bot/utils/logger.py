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
        # Get corresponding Loguru level if it exists
        try:
            level = loguru.logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru.logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logger():
    pathlib.Path(BASE_LOG_DIR).mkdir(parents=True, exist_ok=True)
    fmt = "{time} {name} {level} {message}"
    loguru.logger.add(BASE_LOG_PATH, rotation="512 MB", level="INFO", format=fmt,
                      encoding='utf-8', colorize=True, enqueue=True)
    loguru.logger.add(ERROR_LOG_PATH, rotation="512 MB", level="ERROR", format=fmt,
                      encoding='utf-8', colorize=True, enqueue=True, serialize=True)
    logging.basicConfig(handlers=[InterceptHandler()], level=config.LOGGING_LEVEL)
