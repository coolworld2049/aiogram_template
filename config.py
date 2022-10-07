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
DB_NAME = 'aiogram-template'
TZ = 'Europe/Moscow'

PG_CONFIG = {
    "host": "127.0.0.1",
    "port": 5432,
    "database": DB_NAME,
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
    "state_ttl": 5,  # 5 min
    "data_ttl": 1800,  # 30 min
}
