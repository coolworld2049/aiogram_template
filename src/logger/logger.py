import logging
from logging.handlers import RotatingFileHandler

from bot.config import PROJECT_NAME, LOG_FILE_SIZE_BYTES

logger = logging.Logger(PROJECT_NAME, 'INFO')
filename = 'src/logger/log.log'
file_handler = logging.FileHandler(filename, encoding="utf-8")
stream_handler = logging.StreamHandler()
row_format = "{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}"
file_handler.setFormatter(logging.Formatter(row_format, datefmt='%d/%m/%Y %I:%M:%S %p'))
stream_handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.addHandler(RotatingFileHandler(filename, maxBytes=LOG_FILE_SIZE_BYTES, backupCount=5))
