import logging
import sys

from config import PATH_TO_LOG_FILE


def custom_logger(name: str, level: int | str):
    _logger = logging.Logger(name, level)
    file_handler = logging.FileHandler(PATH_TO_LOG_FILE, encoding="utf-8")
    stream_handler = logging.StreamHandler(sys.stderr)
    row_format = "{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}"
    file_handler.setFormatter(logging.Formatter(row_format, datefmt='%d/%m/%Y %I:%M:%S %p'))
    stream_handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
    _logger.addHandler(file_handler)
    _logger.addHandler(stream_handler)
    return _logger
