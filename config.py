import os

ADMINS = {"I13rsnwhy": "qwerty"}  # <username>: <passphrase>

DEBUG_MODE = False
USE_REDIS = True
USE_SCHEDULER = True

MESSAGE_DELAY = 0.2  # greater than zero
RATE_LIMIT = .50
ITEMS_PER_PAGE = 3

NOTIFY_USER_EVERY_HOURS = 6  # запуск уведомлений для всех пользователей
NOTIFY_USER_MIN = 60  # параметр для проверки времени прошедшего с момента создания заказа

# ----------------------------------------------------------------------------------------

DB_NAME = os.environ['PROJECT_USER']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

PG_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": DB_NAME,
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
}

PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{DB_NAME}"

REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 15,
    "pool_size": 100000,
    "state_ttl": 5,  # 5 min
    "data_ttl": 1800,  # 30 min
}
