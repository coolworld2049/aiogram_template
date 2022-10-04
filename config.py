import json
import os

ADMINS = ['I13rsnwhy']  # nick without @

DEBUG_MODE = True
USE_REDIS = False
USE_LOCAL_SERVER = False
USE_SCHEDULER = False

NOTIFY_USER_EVERY_HOURS = 6  # запуск уведомлений для всех пользователей
NOTIFY_USER_MIN = 60  # параметр для проверки времени прошедшего с момента создания заказа

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
    'database': 'test',
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

MESSAGE_DELAY = 0.1  # greater than zero
ITEMS_PER_PAGE = 3

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

registration_menu_TEXT = 'Чтобы начать пользоваться сервисом, Вам нужно пройти регистрацию.'
main_menu_TEXT = """Вы находитесь в главном меню."""

