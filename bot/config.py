import pathlib
import secrets
from datetime import datetime
from envparse import env

env.read_envfile('.env')

START_POLLING = True
RUN_ON_DOCKER = True

TIMEZONE_UTC = 'Europe/Moscow'

OWNER: int = 5227303016
ADMINS: set = {OWNER}
MANAGERS: set = {1070277776}

USE_DEBUG = False
USE_SCHEDULER = False

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
    "host": 'postgres' if RUN_ON_DOCKER else env.str("PG_HOST", default='127.0.0.1'),
    "port": env.int("PG_PORT", default=5432),
    "database": env.str("PG_DATABASE", default='aiogram_template'),
    "user": env.str("PG_USER", default='postgres'),
    "password": env.str("PG_PASSWORD", default=None),
}

PG_DSN = f"postgresql://{PG_CONFIG['user']}:{PG_CONFIG['password']}" \
         f"@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}"

REDIS_CONFIG = {
    "host": 'redis' if RUN_ON_DOCKER else env.str("REDIS_HOST", default='127.0.0.1'),
    "port": env.int("REDIS_PORT", default=6379),
    "db": env.int("REDIS_DB", default=10),
    "pool_size": env.int("REDIS_POOL", default=10000),
}

REDIS_JOBSTORE_DB = env.int("REDIS_JOBSTORE_DB", default=5)

LOG_PATH = 'journal/logs'
LOG_FILENAME = datetime.today().strftime('%d_%m_%Y')
BASE_LOG_DIR = LOG_PATH + f"/{LOG_FILENAME}"
BASE_LOG_PATH = f"{BASE_LOG_DIR}/{LOG_FILENAME}.log"
ERROR_LOG_PATH = f"{BASE_LOG_DIR}/{LOG_FILENAME}_erorrs.log"

LOG_FILE_SIZE_BYTES = 10 * 104857600
LOGGING_LEVEL = 'INFO'
