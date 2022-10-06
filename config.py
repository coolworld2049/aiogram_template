import os

from filters.command_filters import command_cancel

timezone = "Europe/Moscow"

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
    "database": "test",
    "user": os.environ["PGADMIN"],
    "password": os.environ["PGADMINPASS"],
}

PG_DSN = f"postgresql://{PG_CONFIG['user']}:{PG_CONFIG['password']}" \
         f"@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}"

PATH_TO_LOG_FILE = "log.log"

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


registration_menu_TEXT = "Чтобы начать пользоваться сервисом, Вам нужно пройти регистрацию."
main_menu_TEXT = """Вы находитесь в главном меню."""

help_TEXT = "support text"

user_registration_TEXT = "Введите ваше Имя Фамилия (Пример: Иван Иванов)"

user_state_finish_TEXT = "Данные сохранены"
user_state_incorrect_input_TEXT = "Неправильный формат ввода"

approve_as_admin_incorrect_passphrase_TEXT = 'Кодовое слово не совпало'
admin_panel_TEXT = 'Админ панель'
admin_panel_BTN_TEXT = 'Управление элементами'

admin_items_mgmt_message_IK_TEXT = "Здесь вы можете редактировать список *элементов*"
admin_items_mgmt_message_IK_TEXT_error = "Список элементов отсутствует в базе данных"
admin_items_mgmt_ACTION_TEXT_cancel = f" Отменить действие /{command_cancel.commands[0]}"

admin_items_mgmt_actionADD_TEXT_pre = "ADD ITEM." + admin_items_mgmt_ACTION_TEXT_cancel
admin_items_mgmt_actionUPDATE_TEXT_pre = "UPDATE ITEM." + admin_items_mgmt_ACTION_TEXT_cancel
admin_items_mgmt_actionDELETE_TEXT_pre = "DELETE ITEM." + admin_items_mgmt_ACTION_TEXT_cancel

admin_items_mgmt_actionADD_TEXT_past = "ITEM ADDED."
admin_items_mgmt_actionUPDATE_TEXT_past = "ITEM UPDATED."
admin_items_mgmt_actionDELETE_TEXT_past = "ITEM DELETED."


def account_menu_message_IK_TEXT(user):
    return f"""Ваш аккаунт.

*Имя*: {user['first_name']} {user['last_name']}
*ID*: {user['user_id']}"""


navigation_menu_TEXT = 'Навигация'
navigation_BTN_back = "👈 Назад"
navigation_BTN_back_to_menu = "👈 В меню"

registration_menu_message_IK_TEXT = 'Регистрация'
main_menu_message_IK_BTN_account_TEXT = '👤 Мой аккаунт'
