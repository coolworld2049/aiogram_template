import logging
import pathlib
from datetime import datetime
from logging.handlers import RotatingFileHandler

from bot.config import LOG_FILE_SIZE_BYTES, LOGGING_LEVEL, LOG_PATH, PROJECT_NAME

logger = logging.Logger(PROJECT_NAME, LOGGING_LEVEL)
log_file = f"{datetime.today().strftime('%d_%m_%Y  %I %p')}.log"
pathlib.Path(LOG_PATH).mkdir(parents=True, exist_ok=True)

file_handler = logging.FileHandler(LOG_PATH + log_file, encoding="utf-8")
stream_handler = logging.StreamHandler()
row_format = "{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}"
file_handler.setFormatter(logging.Formatter(row_format, datefmt='%d/%m/%Y %I:%M:%S %p'))
stream_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.addHandler(RotatingFileHandler(LOG_PATH + log_file, maxBytes=LOG_FILE_SIZE_BYTES, backupCount=5))
