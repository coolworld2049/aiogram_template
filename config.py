import json
import os

ADMINS = ['']

DEMO_MODE = False

DEBUG_MODE = False
USE_REDIS = True
USE_SCHEDULER = True

NOTIFY_USER_EVERY_HOURS = 6  # запуск уведомлений для всех пользователей
NOTIFY_USER = 60  # параметр для проверки времени прошедшего с момента создания заказа

PATH_TO_SQL_SCRIPT = 'data/database/bot.sql'
PATH_TO_LOG_FILE = 'log.log'

REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 15,
    'pool_size': 100000,
    'prefix': 'my_fsm_key'
}

PG_CONFIG = {
    'host': '127.0.0.1',
    'port': 5432,
    'database': 'airbot',
    'user': os.environ['PGADMIN'],
    'password': os.environ['PGADMINPASS'],
}

PG_CODEC = {
    'typename': 'json',
    'encoder': json.dumps,
    'decoder': json.loads,
    'schema': 'pg_catalog'
}

PG_DSN = f"postgresql://{PG_CONFIG['user']}:{PG_CONFIG['password']}" \
         f"@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}"

privacy_policy_LINK = 'https//:example.com'

MESSAGE_DELAY = 0.25

ITEMS_PER_PAGE = 3

MIN_BIO_CHARS = 10
MAX_BIO_CHARS = 200

base_commands = \
    [
        {'command': 'start', 'description': 'запуск бота'},
        {'command': 'help', 'description': 'помощь'},
    ]

admin_commands = \
    [
        {'command': 'admin', 'description': 'администратор'},
        {'command': 'get_logs', 'description': 'журнал событий'}
    ]

private_commands = \
    [
        {'command': 'set_sender_bio', 'description': 'обновить инф отправителя'},
        {'command': 'ser_traveler_bio', 'description': 'обновить инф путешественника'},
    ]