import pathlib

BOT_TOKEN = "5654331350:AAE_bFpSBupMmx0Sz_6BOPEIyMVh_67QNPc"
ADMINS = {"I13rsnwhy": "qwerty", 'nickname': 'passphrase'}

DEBUG_MODE = False
USE_REDIS = True
USE_SCHEDULER = False

MESSAGE_DELAY = 0.2
RATE_LIMIT = .50
ITEMS_PER_PAGE = 3

NOTIFY_USER_EVERY_HOURS = 6
NOTIFY_USER_DELTA_MIN = 60

# ----------------------------------------------------------------------------------------

TIMEZONE_UTC = 'Europe/Moscow'

PG_CONFIG = {
    "host": "127.0.0.1",
    "port": 5432,
    "database":  pathlib.Path().cwd().name,
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
    "data_ttl": 1800,
}
