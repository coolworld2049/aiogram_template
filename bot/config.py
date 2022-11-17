import pathlib
from datetime import datetime

from envparse import env

RUN_ON_DOCKER = False

START_POLLING = True
USE_REDIS = True
RESET_USER_STATE_ON_RESTART = False
USE_DEBUG = False

# ----------------------------------------------------------------------------------------------------------------------

OWNER: int = 5227303016
ADMINS: set = {OWNER}

MESSAGE_DELAY = 0.2
RATE_LIMIT = 0.50
# ----------------------------------------------------------------------------------------------------------------------

ITEMS_PER_PAGE = 3

env.read_envfile('.env')

ROOT_DIRECTORY = pathlib.Path(__file__).parent.parent
PROJECT_NAME = pathlib.Path().cwd().name

BOT_TOKEN = env.str("BOT_TOKEN")

PG_CONFIG = {
    "host": 'postgres-ptb' if RUN_ON_DOCKER else env.str("PG_HOST", default='127.0.0.1'),
    "port": env.int("PG_DOCKER_PORT", default=5433) if RUN_ON_DOCKER else env.int("PG_PORT", default=5432),
    "database": env.str("PG_DATABASE", default='postgres'),
    "user": env.str("PG_USER", default='postgres'),
    "password": env.str("PG_PASSWORD", default=None),
}

PG_DSN = f"postgresql://{PG_CONFIG['user']}:{PG_CONFIG['password']}" \
         f"@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}"

REDIS_CONFIG = {
    "host": 'redis-ptb' if RUN_ON_DOCKER else env.str("REDIS_HOST", default='127.0.0.1'),
    "port": env.int("REDIS_DOCKER_PORT", default=6379) if RUN_ON_DOCKER else env.int("REDIS_PORT", default=6380),
    "db": env.int("REDIS_DB", default=10),
    "pool_size": env.int("REDIS_POOL", default=10000),
}


LOG_PATH = 'journal/logs'
LOG_FILENAME = datetime.today().strftime('%d_%m_%Y')
BASE_LOG_DIR = LOG_PATH + f"/{LOG_FILENAME}"
BASE_LOG_PATH = f"{BASE_LOG_DIR}/{LOG_FILENAME}.log"
ERROR_LOG_PATH = f"{BASE_LOG_DIR}/{LOG_FILENAME}_erorrs.log"

LOG_FILE_SIZE_BYTES = 10 * 104857600
LOGGING_LEVEL = 'INFO'
