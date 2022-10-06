import os

PROJECT_NAME = os.environ['PROJECT_NAME']
PROJECT_USER = os.environ['PROJECT_USER']
DB_NAME = os.environ['PROJECT_NAME']
DB_SCHEMA = os.environ['DB_SCHEMA']
PGUSER = os.environ['PGUSER']
PGPASS = os.environ['PGPASS']
TZ = os.environ['TZ']


ADMINS = {"I13rsnwhy": "qwerty"}  # <username>: <passphrase>

DEBUG_MODE = False
USE_LOCAL_SERVER = False
USE_REDIS = True
USE_SCHEDULER = True

MESSAGE_DELAY = 0.2  # greater than zero
ITEMS_PER_PAGE = 3

NOTIFY_USER_EVERY_HOURS = 6  # запуск уведомлений для всех пользователей
NOTIFY_USER_MIN = 60  # параметр для проверки времени прошедшего с момента создания заказа

RATE_LIMIT = .50

PATH_TO_LOG_FILE = "log.log"

REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 15,
    "pool_size": 100000,
    "state_ttl": 5,  # 5 min
    "data_ttl": 1800,  # 30 min
}

PG_CONFIG = {
    "host": "127.0.0.1",
    "port": 5432,
    "database": DB_NAME,
    "user": PGUSER,
    "password": PGPASS,
}

PG_DSN = f"postgresql://{PGUSER}:{PGPASS}@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{DB_NAME}"

base_commands = \
    [
        {"command": "start", "description": "запуск бота"},
        {"command": "help", "description": "помощь"},
    ]

admin_commands = \
    [
        {"command": "admin", "description": "администратор"},
        {"command": "get_logs", "description": "журнал событий"}
    ]
