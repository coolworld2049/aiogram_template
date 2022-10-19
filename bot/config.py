import pathlib
import secrets
from datetime import datetime
from envparse import env

START_POLLING = True

TIMEZONE_UTC = 'Europe/Moscow'

OWNER: int = 5227303016
ADMINS: set = {OWNER}
MANAGERS: set = {1070277776}

USE_DEBUG = False
USE_SCHEDULER = True

MESSAGE_DELAY = 0.2
RATE_LIMIT = .50
ITEMS_PER_PAGE = 3

NOTIFY_USER_EVERY_HOURS = 6

# ----------------------------------------------------------------------------------------

ROOT_DIRECTORY = pathlib.Path(__file__).parent.parent
PROJECT_NAME = pathlib.Path().cwd().name

BOT_TOKEN = env.str("BOT_TOKEN")
BOT_PUBLIC_PORT = env.int("BOT_PUBLIC_PORT", default=8080)

DOMAIN = env.str("DOMAIN", default="example.com")
SECRET_KEY = secrets.token_urlsafe(48)
WEBHOOK_BASE_PATH = env.str("WEBHOOK_BASE_PATH", default="/webhook")
WEBHOOK_PATH = f"{WEBHOOK_BASE_PATH}/{SECRET_KEY}"
WEBHOOK_URL = f"https://{DOMAIN}{WEBHOOK_PATH}"


PG_CONFIG = {
    "host": "127.0.0.1",
    "port": 5432,
    "database": PROJECT_NAME,
    "user": 'postgres',
    "password": 'postgres',
}

PG_DSN = f"postgresql://{PG_CONFIG['user']}:{PG_CONFIG['password']}" \
         f"@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}"

REDIS_CONFIG = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 15,
    "pool_size": 100000,
    "state_ttl": 300,
}

REDIS_JOBSTORE = 10

LOG_PATH = 'journal/logs'
LOG_FILENAME = datetime.today().strftime('%d_%m_%Y')
BASE_LOG_DIR = LOG_PATH + f"/{LOG_FILENAME}"
BASE_LOG_PATH = f"{BASE_LOG_DIR}/{LOG_FILENAME}.log"
ERROR_LOG_PATH = f"{BASE_LOG_DIR}/{LOG_FILENAME}_erorrs.log"

LOG_FILE_SIZE_BYTES = 10 * 104857600
LOGGING_LEVEL = 'INFO'