import logging
import pathlib

import loguru

from bot import config
from bot.config import LOG_PATH, LOG_FILE_NAME, LOG_FILE_NAME_ERROR


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
    base_log_path = LOG_PATH + '/' + LOG_FILE_NAME
    error_log_path = LOG_PATH + '/' + LOG_FILE_NAME_ERROR
    pathlib.Path(base_log_path).mkdir(parents=True, exist_ok=True)
    pathlib.Path(error_log_path).mkdir(parents=True, exist_ok=True)

    fmt = "{time} {name} {level} {message}"
    loguru.logger.add(base_log_path + '/' + LOG_FILE_NAME + '.log', rotation="1024 MB", level="INFO", format=fmt,
                      encoding='utf-8', colorize=True, enqueue=True)
    loguru.logger.add(error_log_path + '/' + LOG_FILE_NAME + '.log', rotation="1024 MB", level="ERROR", format=fmt,
                      encoding='utf-8', colorize=True, enqueue=True, serialize=True)
    logging.basicConfig(handlers=[InterceptHandler()], level=config.LOGGING_LEVEL)
