import pathlib

ROOT_DIRECTORY = pathlib.Path(__file__).parent.parent
PROJECT_NAME = pathlib.Path().cwd().name

BOT_TOKEN = ""

OWNER: int = 5227303016
ADMINS: set = {OWNER}
MANAGERS: set = {1070277776}

DEBUG_MODE = False
USE_REDIS = True
USE_SCHEDULER = False

MESSAGE_DELAY = 0.01
RATE_LIMIT = .50
ITEMS_PER_PAGE = 3

NOTIFY_USER_EVERY_HOURS = 6
NOTIFY_USER_DELTA_MIN = 60

LOG_PATH = 'src/services/journal/logs/'
LOG_FILE_SIZE_BYTES = 10 * 104857600
LOGGING_LEVEL = 'INFO'

REDIS_CONFIG = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 15,
    "pool_size": 100000,
    "state_ttl": 300,
    "data_ttl": 1800,
}

common_commands = \
    [
        {"command": "start", "description": "запуск бота"},
        {"command": "restart", "description": "перезапуск бота"},
        {"command": "help", "description": "помощь"},
    ]

admin_commands = \
    [
        {"command": "admin", "description": "администратор"},
        {"command": "get_logs", "description": "журнал событий"}
    ]

manager_commands = \
    [
        {"command": "manager", "description": "менеджер"}
    ]

# ----------------------------------------------------------------------------------------

TIMEZONE_UTC = 'Europe/Moscow'

PG_CONFIG = {
    "host": "127.0.0.1",
    "port": 5432,
    "database": PROJECT_NAME,
    "user": 'postgres',
    "password": 'postgres',
}

PG_DSN = f"postgresql://{PG_CONFIG['user']}:{PG_CONFIG['password']}" \
         f"@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}"
