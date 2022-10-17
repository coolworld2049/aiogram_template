import logging
import pathlib
from datetime import datetime
from logging.handlers import RotatingFileHandler

from bot.config import LOG_FILE_SIZE_BYTES, LOGGING_LEVEL, LOG_PATH, PROJECT_NAME

pathlib.Path(LOG_PATH).mkdir(parents=True, exist_ok=True)


logger = logging.Logger(PROJECT_NAME, LOGGING_LEVEL)
file_name = f"{datetime.today().strftime('%d_%m_%Y')}.log"
row_format = "{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}"
file_handler = logging.FileHandler(LOG_PATH + file_name, encoding="utf-8")
file_handler.setFormatter(logging.Formatter(row_format, datefmt='%d/%m/%Y %I:%M:%S %p'))
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.addHandler(RotatingFileHandler(LOG_PATH + file_name, maxBytes=LOG_FILE_SIZE_BYTES, backupCount=5))
