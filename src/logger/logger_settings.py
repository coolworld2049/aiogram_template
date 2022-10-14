import logging
from logging.handlers import RotatingFileHandler

from bot.config import LOG_FILE_SIZE_BYTES


def custom_logger(name: str, level: int | str, filename: str):
    _logger = logging.Logger(name, level)
    file_handler = logging.FileHandler(filename, encoding="utf-8")
    stream_handler = logging.StreamHandler()
    row_format = "{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}"
    file_handler.setFormatter(logging.Formatter(row_format, datefmt='%d/%m/%Y %I:%M:%S %p'))
    stream_handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
    _logger.addHandler(file_handler)
    _logger.addHandler(stream_handler)
    _logger.addHandler(RotatingFileHandler(filename, maxBytes=LOG_FILE_SIZE_BYTES, backupCount=5))
    return _logger
