from bot.filters.command_filters import command_cancel

registration_menu_TEXT = "Чтобы начать пользоваться сервисом, Вам нужно пройти регистрацию."
registration_menu_message_IK_TEXT = 'Регистрация'

main_menu_TEXT = """Вы находитесь в главном меню."""
main_menu_message_IK_BTN_account_TEXT = '👤 Мой аккаунт'

help_TEXT = "support text"

user_registration_TEXT = "Введите ваше Имя Фамилия (Пример: Иван Иванов)"
user_state_finish_TEXT = "Данные сохранены"
user_state_incorrect_input_TEXT = "Неправильный формат ввода"

admin_panel_TEXT = 'Админ панель'
admin_panel_BTN_items_mgmt_TEXT = 'Управление элементами'
admin_panel_BTN_server_stats_TEXT = 'Состояние сервера'

items_mgmt_message_IK_TEXT = "Здесь вы можете редактировать список *элементов*"
items_mgmt_message_IK_TEXT_error = "Список элементов отсутствует в базе данных"
items_mgmt_ACTION_TEXT_cancel = f" Отменить действие /{command_cancel.commands[0]}"

items_mgmt_action_ADD_TEXT_pre = "ADD ITEM." + items_mgmt_ACTION_TEXT_cancel
items_mgmt_action_UPDATE_TEXT_pre = "UPDATE ITEM." + items_mgmt_ACTION_TEXT_cancel
items_mgmt_action_DELETE_TEXT_pre = "DELETE ITEM." + items_mgmt_ACTION_TEXT_cancel

items_mgmt_action_ADD_TEXT_past = "ITEM ADDED."
items_mgmt_action_UPDATE_TEXT_past = "ITEM UPDATED."
items_mgmt_action_DELETE_TEXT_past = "ITEM DELETED."


def account_menu_message_IK_TEXT(user):
    return f"""Ваш аккаунт.

*Имя*: {user['first_name']} {user['last_name']}
*ID*: {user['user_id']}"""


navigation_menu_TEXT = 'Навигация'
navigation_BTN_back = "👈 Назад"
navigation_BTN_back_to_menu = "👈 В меню"
