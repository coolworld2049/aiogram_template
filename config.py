import json
import os

from filters.command_filters import command_cancel

ADMINS = ["I13rsnwhy"]  # nick without @

DEBUG_MODE = True
USE_REDIS = False
USE_LOCAL_SERVER = False
USE_SCHEDULER = False

NOTIFY_USER_EVERY_HOURS = 6  # запуск уведомлений для всех пользователей
NOTIFY_USER_MIN = 60  # параметр для проверки времени прошедшего с момента создания заказа

PATH_TO_LOG_FILE = "log.log"

REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 15,
    "pool_size": 100000,
    "prefix": "my_fsm_key"
}

PG_CONFIG = {
    "host": "127.0.0.1",
    "port": 5432,
    "database": "test",
    "user": os.environ["PGADMIN"],
    "password": os.environ["PGADMINPASS"],
}

PG_CODEC = {
    "typename": "json",
    "encoder": json.dumps,
    "decoder": json.loads,
    "schema": "pg_catalog"
}

PG_DSN = f"postgresql://{PG_CONFIG['user']}:{PG_CONFIG['password']}" \
         f"@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}"

MESSAGE_DELAY = 0.1  # greater than zero
ITEMS_PER_PAGE = 3

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
